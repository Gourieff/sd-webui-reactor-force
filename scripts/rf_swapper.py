import os
from dataclasses import dataclass
from typing import List, Union, Tuple
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image

import insightface
# import onnxruntime as ort

from modules.face_restoration import FaceRestoration
try: # A1111
    from modules import codeformer_model
except: # SD.Next
    from modules.postprocess import codeformer_model
from modules.upscaler import UpscalerData
from modules.shared import state
from scripts.rf_logger import logger
try:
    from modules.paths_internal import models_path
except:
    try:
        from modules.paths import models_path
    except:
        model_path = os.path.abspath("models")

import warnings

np.warnings = warnings
np.warnings.filterwarnings('ignore')

providers = ["CUDAExecutionProvider"]


@dataclass
class EnhancementOptions:
    do_restore_first: bool = True
    scale: int = 1
    upscaler: UpscalerData = None
    upscale_visibility: float = 0.5
    face_restorer: FaceRestoration = None
    restorer_visibility: float = 0.5
    codeformer_weight: float = 0.5


MESSAGED_STOPPED = False
MESSAGED_SKIPPED = False

def reset_messaged():
    global MESSAGED_STOPPED, MESSAGED_SKIPPED
    if not state.interrupted:
        MESSAGED_STOPPED = False
    if not state.skipped:
        MESSAGED_SKIPPED = False

def check_process_halt(msgforced: bool = False):
    global MESSAGED_STOPPED, MESSAGED_SKIPPED
    if state.interrupted:
        if not MESSAGED_STOPPED or msgforced:
            logger.status("Stopped by User")
            MESSAGED_STOPPED = True
        return True
    if state.skipped:
        if not MESSAGED_SKIPPED or msgforced:
            logger.status("Skipped by User")
            MESSAGED_SKIPPED = True
        return True
    return False


FS_MODEL = None
CURRENT_FS_MODEL_PATH = None

ANALYSIS_MODEL = None


@lru_cache(maxsize=3)
def getAnalysisModel(det_size: Tuple[int, int] = (640, 640)):
    global ANALYSIS_MODEL
    if ANALYSIS_MODEL is None:
        ANALYSIS_MODEL = insightface.app.FaceAnalysis(
            name="buffalo_l", providers=providers, root=os.path.join(models_path, "insightface") # note: allowed_modules=['detection', 'genderage']
        )
    ANALYSIS_MODEL.prepare(ctx_id=0, det_size=det_size)
    return ANALYSIS_MODEL


@lru_cache(maxsize=1)
def getFaceSwapModel(model_path: str):
    global FS_MODEL
    global CURRENT_FS_MODEL_PATH
    if CURRENT_FS_MODEL_PATH is None or CURRENT_FS_MODEL_PATH != model_path:
        # ort.InferenceSession(model_path, providers=providers)
        CURRENT_FS_MODEL_PATH = model_path
        FS_MODEL = insightface.model_zoo.get_model(model_path, providers=providers)

    return FS_MODEL


def restore_face(image: Image, enhancement_options: EnhancementOptions):
    result_image = image

    if check_process_halt(msgforced=True):
        return result_image
    
    if enhancement_options.face_restorer is not None:
        original_image = result_image.copy()
        logger.status("Restoring the face with %s", enhancement_options.face_restorer.name())
        numpy_image = np.array(result_image)
        if enhancement_options.face_restorer.name() == "CodeFormer":
            numpy_image = codeformer_model.codeformer.restore(
                numpy_image, w=enhancement_options.codeformer_weight
            )
        else:
            numpy_image = enhancement_options.face_restorer.restore(numpy_image)
        restored_image = Image.fromarray(numpy_image)
        result_image = Image.blend(
            original_image, restored_image, enhancement_options.restorer_visibility
        )
    
    return result_image

def upscale_image(image: Image, enhancement_options: EnhancementOptions):
    result_image = image

    if check_process_halt(msgforced=True):
        return result_image
    
    if enhancement_options.upscaler is not None and enhancement_options.upscaler.name != "None":
        original_image = result_image.copy()
        logger.status(
            "Upscaling with %s scale = %s",
            enhancement_options.upscaler.name,
            enhancement_options.scale,
        )
        result_image = enhancement_options.upscaler.scaler.upscale(
            original_image, enhancement_options.scale, enhancement_options.upscaler.data_path
        )
        if enhancement_options.scale == 1:
            result_image = Image.blend(
                original_image, result_image, enhancement_options.upscale_visibility
            )
    
    return result_image

def enhance_image(image: Image, enhancement_options: EnhancementOptions):
    result_image = image
    
    if check_process_halt(msgforced=True):
        return result_image
    
    if enhancement_options.do_restore_first:
        
        result_image = restore_face(result_image, enhancement_options)
        result_image = upscale_image(result_image, enhancement_options)

    else:

        result_image = upscale_image(result_image, enhancement_options)
        result_image = restore_face(result_image, enhancement_options)

    return result_image

def get_gender(face, face_index):
    gender = [
        x.sex
        for x in face
    ]
    gender.reverse()
    try:
        face_gender = gender[face_index]
    except:
        logger.error("Gender Detection: No face with index = %s was found", face_index)
        return "None"
    return face_gender

def get_face_gender(
        face,
        face_index,
        gender_condition,
        operated: str,
        gender_detected,
):
    face_gender = gender_detected
    if face_gender == "None":
        return None, 0
    logger.status("%s Face %s: Detected Gender -%s-", operated, face_index, face_gender)
    if (gender_condition == 1 and face_gender == "F") or (gender_condition == 2 and face_gender == "M"):
        logger.status("OK - Detected Gender matches Condition")
        try:
            return sorted(face, key=lambda x: x.bbox[0])[face_index], 0
        except IndexError:
            return None, 0
    else:
        logger.status("WRONG - Detected Gender doesn't match Condition")
        return sorted(face, key=lambda x: x.bbox[0])[face_index], 1

def get_face_age(face, face_index):
    age = [
        x.age
        for x in face
    ]
    age.reverse()
    try:
        face_age = age[face_index]
    except:
        logger.error("Age Detection: No face with index = %s was found", face_index)
        return "None"
    return face_age

def half_det_size(det_size):
    logger.status("Trying to halve 'det_size' parameter")
    return (det_size[0] // 2, det_size[1] // 2)

def analyze_faces(img_data: np.ndarray, det_size=(640, 640)):
    face_analyser = getAnalysisModel(det_size)
    return face_analyser.get(img_data)

def get_face_single(img_data: np.ndarray, face, face_index=0, det_size=(640, 640), gender_source=0, gender_target=0):

    buffalo_path = os.path.join(models_path, "insightface/models/buffalo_l.zip")
    if os.path.exists(buffalo_path):
        os.remove(buffalo_path)

    face_age = "None"
    try:
        face_age = get_face_age(face, face_index)
    except:
        logger.error("Cannot detect any Age for Face index = %s", face_index)
    
    face_gender = "None"
    try:
        face_gender = get_gender(face, face_index)
        gender_detected = face_gender
        face_gender = "Female" if face_gender == "F" else ("Male" if face_gender == "M" else "None")
    except:
        logger.error("Cannot detect any Gender for Face index = %s", face_index)
    
    if gender_source != 0:
        if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
            det_size_half = half_det_size(det_size)
            return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)
        faces, wrong_gender = get_face_gender(face,face_index,gender_source,"Source",gender_detected)
        return faces, wrong_gender, face_age, face_gender

    if gender_target != 0:
        if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
            det_size_half = half_det_size(det_size)
            return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)
        faces, wrong_gender = get_face_gender(face,face_index,gender_target,"Target",gender_detected)
        return faces, wrong_gender, face_age, face_gender
    
    if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
        det_size_half = half_det_size(det_size)
        return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)

    try:
        return sorted(face, key=lambda x: x.bbox[0])[face_index], 0, face_age, face_gender
    except IndexError:
        return None, 0, face_age, face_gender


def swap_face(
    source_img: Image.Image,
    target_img: Image.Image,
    model: Union[str, None] = None,
    source_faces_index: List[int] = [0],
    faces_index: List[int] = [0],
    enhancement_options: Union[EnhancementOptions, None] = None,
    gender_source: int = 0,
    gender_target: int = 0,
):
    result_image = target_img
    
    if check_process_halt():
        return result_image, [], 0
    
    if model is not None:

        if isinstance(source_img, str):  # source_img is a base64 string
            import base64, io
            if 'base64,' in source_img:  # check if the base64 string has a data URL scheme
                # split the base64 string to get the actual base64 encoded image data
                base64_data = source_img.split('base64,')[-1]
                # decode base64 string to bytes
                img_bytes = base64.b64decode(base64_data)
            else:
                # if no data URL scheme, just decode
                img_bytes = base64.b64decode(source_img)
            
            source_img = Image.open(io.BytesIO(img_bytes))
            
        source_img = cv2.cvtColor(np.array(source_img), cv2.COLOR_RGB2BGR)
        target_img = cv2.cvtColor(np.array(target_img), cv2.COLOR_RGB2BGR)

        output: List = []
        output_info: str = ""
        swapped = 0

        logger.status("Analyzing Source Image...")
        source_faces = analyze_faces(source_img)

        if source_faces is not None:

            logger.status("Analyzing Target Image...")
            target_faces = analyze_faces(target_img)

            logger.status("Detecting Source Face, Index = %s", source_faces_index[0])        
            source_face, wrong_gender, source_age, source_gender = get_face_single(source_img, source_faces, face_index=source_faces_index[0], gender_source=gender_source)
            if source_age != "None" or source_gender != "None":
                logger.status("Detected: -%s- y.o. %s", source_age, source_gender)

            output_info = f"SourceFaceIndex={source_faces_index[0]};Age={source_age};Gender={source_gender}\n"
            output.append(output_info)

            if len(source_faces_index) != 0 and len(source_faces_index) != 1 and len(source_faces_index) != len(faces_index):
                logger.status("Source Faces must have no entries (default=0), one entry, or same number of entries as target faces.")
            elif source_face is not None:
            
                result = target_img
                face_swapper = getFaceSwapModel(model)

                source_face_idx = 0

                for face_num in faces_index:
                    if check_process_halt():
                        return result_image, [], 0
                    if len(source_faces_index) > 1 and source_face_idx > 0:
                        logger.status("Detecting Source Face, Index = %s", source_faces_index[source_face_idx])
                        source_face, wrong_gender, source_age, source_gender = get_face_single(source_img, source_faces, face_index=source_faces_index[source_face_idx], gender_source=gender_source)
                        if source_age != "None" or source_gender != "None":
                            logger.status("Detected: -%s- y.o. %s", source_age, source_gender)

                        output_info = f"SourceFaceIndex={source_faces_index[source_face_idx]};Age={source_age};Gender={source_gender}\n"
                        output.append(output_info)

                    source_face_idx += 1

                    if source_face is not None and wrong_gender == 0:
                        logger.status("Detecting Target Face, Index = %s", face_num)
                        target_face, wrong_gender, target_age, target_gender = get_face_single(target_img, target_faces, face_index=face_num, gender_target=gender_target)
                        if target_age != "None" or target_gender != "None":
                            logger.status("Detected: -%s- y.o. %s", target_age, target_gender)

                        output_info = f"TargetFaceIndex={face_num};Age={target_age};Gender={target_gender}\n"
                        output.append(output_info)
                        
                        if target_face is not None and wrong_gender == 0:
                            logger.status("Swapping Source into Target")
                            result = face_swapper.get(result, target_face, source_face)
                            swapped += 1
                        
                        elif wrong_gender == 1:
                            wrong_gender = 0
                            
                            if source_face_idx == len(source_faces_index):
                                result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                                
                                if enhancement_options is not None and len(source_faces_index) > 1:
                                    result_image = enhance_image(result_image, enhancement_options)
                                
                                return result_image, output, swapped
                        
                        else:
                            logger.status(f"No target face found for {face_num}")
                    
                    elif wrong_gender == 1:
                        wrong_gender = 0
                        
                        if source_face_idx == len(source_faces_index):
                            result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                            
                            if enhancement_options is not None and len(source_faces_index) > 1:
                                result_image = enhance_image(result_image, enhancement_options)
                            
                            return result_image, output, swapped
                    
                    else:
                        logger.status(f"No source face found for face number {source_face_idx}.")

                result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                
                if enhancement_options is not None and swapped > 0:
                    result_image = enhance_image(result_image, enhancement_options)

            else:
                logger.status("No source face(s) in the provided Index")
        else:
            logger.status("No source face(s) found")
    
    return result_image, output, swapped
