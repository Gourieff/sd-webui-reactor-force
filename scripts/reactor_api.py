'''
Thanks SpenserCai for the original version of the roop api script
-----------------------------------
--- ReActor External API v1.0.8a ---
-----------------------------------
'''
import os, glob
from datetime import datetime, date
from fastapi import FastAPI, Body
# from fastapi.exceptions import HTTPException
# from io import BytesIO
# from PIL import Image
# import base64
# import numpy as np
# import cv2
import asyncio
from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures.process import ProcessPoolExecutor
# from contextlib import asynccontextmanager
# import multiprocessing

# from modules.api.models import *
from modules import scripts, shared
from modules.api import api

import gradio as gr

from scripts.reactor_swapper import EnhancementOptions, blend_faces, swap_face, DetectionOptions
from scripts.reactor_logger import logger
from scripts.reactor_helpers import get_facemodels


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.executor = ProcessPoolExecutor(max_workers=4)
#     yield
#     app.state.executor.shutdown()

# app = FastAPI(lifespan=lifespan)

# def run_app(a: FastAPI):
#     global app
#     a = app
#     return a

# _executor_tp = ThreadPoolExecutor(max_workers=8)
# def entry_point():
#     _executor_pp = ProcessPoolExecutor(max_workers=8)
# pool = multiprocessing.Pool(4)

async def run_event(app, fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, fn, *args)


def default_file_path():
    time = datetime.now()
    today = date.today()
    current_date = today.strftime('%Y-%m-%d')
    current_time = time.strftime('%H-%M-%S')
    output_file = 'output_'+current_date+'_'+current_time+'.png'
    return os.path.join(os.path.abspath("outputs/api"), output_file)

def get_face_restorer(name):
    for restorer in shared.face_restorers:
        if restorer.name() == name:
            return restorer
    return None

def get_upscaler(name):
    for upscaler in shared.sd_upscalers:
        if upscaler.name == name:
            return upscaler
    return None

def get_models():
    models_path = os.path.join(scripts.basedir(), "models/insightface/*")
    models = glob.glob(models_path)
    models = [x for x in models if x.endswith(".onnx") or x.endswith(".pth")]
    return models

def get_full_model(model_name):
    models = get_models()
    for model in models:
        model_path = os.path.split(model)
        if model_path[1] == model_name:
            return model
    return None

# def decode_base64_to_image_rgba(encoding):
#     if encoding.startswith("data:image/"):
#         encoding = encoding.split(";")[1].split(",")[1]
#     try:
#         im_bytes = base64.b64decode(encoding)
#         im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
#         img = cv2.imdecode(im_arr, flags=cv2.IMREAD_UNCHANGED)
#         img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
#         image = Image.fromarray(img, mode="RGBA")
#         return image
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Invalid encoded image") from e

def reactor_api(_: gr.Blocks, app: FastAPI):
    app.state.executor = ThreadPoolExecutor(max_workers=8)
    @app.post("/reactor/image")
    async def reactor_image(
        source_image: str = Body("",title="Source Face Image"),
        target_image: str = Body("",title="Target Image"),
        source_faces_index: list[int] = Body([0],title="Comma separated face number(s) from swap-source image"),
        face_index: list[int] = Body([0],title="Comma separated face number(s) for target image (result)"),
        upscaler: str = Body("None",title="Upscaler"),
        scale: float = Body(1,title="Scale by"),
        upscale_visibility: float = Body(1,title="Upscaler visibility (if scale = 1)"),
        face_restorer: str = Body("None",title="Restore Face: 0 - None; 1 - CodeFormer; 2 - GFPGA"),
        restorer_visibility: float = Body(1,title="Restore visibility value"),
        codeformer_weight: float = Body(0.5,title="CodeFormer Weight"),
        restore_first: int = Body(1,title="Restore face -> Then upscale, 1 - True, 0 - False"),
        model: str = Body("inswapper_128.onnx",title="Model"),
        gender_source: int = Body(0,title="Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)"),
        gender_target: int = Body(0,title="Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)"),
        save_to_file: int = Body(0,title="Save Result to file, 0 - No, 1 - Yes"),
        result_file_path: str = Body("",title="(if 'save_to_file = 1') Result file path"),
        device: str = Body("CPU",title="CPU or CUDA (if you have it)"),
        mask_face: int = Body(0,title="Face Mask Correction, 1 - True, 0 - False"),
        select_source: int = Body(0,title="Select Source, 0 - Image, 1 - Face Model, 2 - Source Folder"),
        face_model: str = Body("None",title="Filename of the face model (from 'models/reactor/faces'), e.g. elena.safetensors"),
        source_folder: str = Body("",title="The path to the folder containing source faces images"),
        random_image: int = Body(0,title="Randomly select an image from the path"),
        upscale_force: int = Body(0,title="Force Upscale even if no face found"),
        det_thresh: float = Body(0.5,title="Face Detection Threshold"),
        det_maxnum: int = Body(0,title="Maximum number of faces to detect (0 is unlimited)"),
    ):
        s_image = api.decode_base64_to_image(source_image) if select_source == 0 else None
        t_image = api.decode_base64_to_image(target_image)

        if t_image.mode == 'RGBA':
            _, _, _, alpha = t_image.split()
        else:
            alpha = None
        
        sf_index = source_faces_index
        f_index = face_index
        gender_s = gender_source
        gender_t = gender_target
        restore_first_bool = True if restore_first == 1 else False
        mask_face = True if mask_face == 1 else False
        random_image = False if random_image == 0 else True
        upscale_force = False if upscale_force == 0 else True
        up_options = EnhancementOptions(do_restore_first=restore_first_bool, scale=scale, upscaler=get_upscaler(upscaler), upscale_visibility=upscale_visibility,face_restorer=get_face_restorer(face_restorer),restorer_visibility=restorer_visibility,codeformer_weight=codeformer_weight,upscale_force=upscale_force)
        det_options = DetectionOptions(det_thresh=det_thresh, det_maxnum=det_maxnum)
        use_model = get_full_model(model)
        if use_model is None:
            Exception("Model not found")
        
        args = [s_image, t_image, use_model, sf_index, f_index, up_options, gender_s, gender_t, True, True, device, mask_face, select_source, face_model, source_folder, None, random_image,det_options]
        # result,_,_ = pool.map(swap_face, *args)
        result,_,_ = await run_event(app,swap_face,*args)
        # result,_,_ = swap_face(s_image, t_image, use_model, sf_index, f_index, up_options, gender_s, gender_t, True, True, device, mask_face, select_source, face_model, source_folder, None, random_image,det_options)

        if alpha is not None:
            result = result.convert("RGBA")
            result.putalpha(alpha)

        if save_to_file == 1:
            if result_file_path == "":
                result_file_path = default_file_path()
            try:
                file_format = os.path.split(result_file_path)[1].split(".")[1]
                result.save(result_file_path, format=file_format)
                logger.status("Result has been saved to: %s", result_file_path)
            except Exception as e:
                logger.error("Error while saving result: %s",e)
        return {"image": api.encode_pil_to_base64(result)}

    @app.get("/reactor/models")
    async def reactor_models():
        model_names = [os.path.split(model)[1] for model in get_models()]
        return {"models": model_names}
    
    @app.get("/reactor/upscalers")
    async def reactor_upscalers():
        names = [upscaler.name for upscaler in shared.sd_upscalers]
        return {"upscalers": names}
    
    @app.get("/reactor/facemodels")
    async def reactor_facemodels():
        facemodels = [os.path.split(model)[1].split(".")[0] for model in get_facemodels()]
        return {"facemodels": facemodels}

    @app.post("/reactor/facemodels")
    async def reactor_facemodels_build(
        source_images: list[str] = Body([""],title="Source Face Image List"),
        name: str = Body("",title="Face Model Name"),
        compute_method: int = Body(0,title="Compute Method (Mean, Median, Mode)"),
    ):
        images = [api.decode_base64_to_image(img) for img in source_images]
        blend_faces(images, name, compute_method, False, is_api=True)
        return {"facemodels": [os.path.split(model)[1].split(".")[0] for model in get_facemodels()]}

try:
    import modules.script_callbacks as script_callbacks
    script_callbacks.on_app_started(reactor_api)
except:
    pass
