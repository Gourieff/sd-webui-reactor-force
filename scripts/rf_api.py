'''
Thanks SpenserCai for the original version of the roop api script
-----------------------------------
--- ReActor External API v1.0.1 ---
-----------------------------------
'''
import os, glob
from datetime import datetime, date
from fastapi import FastAPI, Body

# from modules.api.models import *
from modules import scripts, shared
from modules.api import api

import gradio as gr

from scripts.rf_swapper import EnhancementOptions, swap_face
from scripts.rf_logger import logger


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

def reactor_api(_: gr.Blocks, app: FastAPI):
    @app.post("/reactor/image")
    async def reactor_image(
        source_image: str = Body("",title="Source Face Image"),
        target_image: str = Body("",title="Target Image"),
        source_faces_index: list[int] = Body([0],title="Comma separated face number(s) from swap-source image"),
        face_index: list[int] = Body([0],title="Comma separated face number(s) for target image (result)"),
        upscaler: str = Body("None",title="Upscaler"),
        scale: int = Body(1,title="Scale by"),
        upscale_visibility: float = Body(1,title="Upscaler visibility (if scale = 1)"),
        face_restorer: str = Body("None",title="Restore Face: 0 - None; 1 - CodeFormer; 2 - GFPGA"),
        restorer_visibility: float = Body(1,title="Restore visibility value"),
        codeformer_weight: float = Body(0.5,title="CodeFormer Weight"),
        restore_first: int = Body(1,title="Restore face -> Then upscale, 1 - True, 0 - False"),
        model: str = Body("inswapper_128.onnx",title="Model"),
        gender_source: int = Body(0,title="Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)"),
        gender_target: int = Body(0,title="Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)"),
        save_to_file: int = Body(0,title="Save Result to file, 0 - No, 1 - Yes"),
        result_file_path: str = Body("",title="(if 'save_to_file = 1') Result file path")
    ):
        s_image = api.decode_base64_to_image(source_image)
        t_image = api.decode_base64_to_image(target_image)
        sf_index = source_faces_index
        f_index = face_index
        gender_s = gender_source
        gender_t = gender_target
        restore_first_bool = True if restore_first == 1 else False
        up_options = EnhancementOptions(do_restore_first=restore_first_bool, scale=scale, upscaler=get_upscaler(upscaler), upscale_visibility=upscale_visibility,face_restorer=get_face_restorer(face_restorer),restorer_visibility=restorer_visibility,codeformer_weight=codeformer_weight)
        use_model = get_full_model(model)
        if use_model is None:
            Exception("Model not found")
        result = swap_face(s_image, t_image, use_model, sf_index, f_index, up_options, gender_s, gender_t)
        if save_to_file == 1:
            if result_file_path == "":
                result_file_path = default_file_path()
            try:
                result[0].save(result_file_path, format='PNG')
                logger.status("Result has been saved to: %s", result_file_path)
            except Exception as e:
                logger.error("Error while saving result: %s",e)
        return {"image": api.encode_pil_to_base64(result[0])}

    @app.get("/reactor/models")
    async def reactor_models():
        model_names = [os.path.split(model)[1] for model in get_models()]
        return {"models": model_names}
    
    @app.get("/reactor/upscalers")
    async def reactor_upscalers():
        names = [upscaler.name for upscaler in shared.sd_upscalers]
        return {"upscalers": names}

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(reactor_api)
except:
    pass
