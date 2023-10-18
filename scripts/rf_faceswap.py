import os, glob
import gradio as gr
from PIL import Image

from typing import List

import modules.scripts as scripts
from modules.upscaler import Upscaler, UpscalerData
from modules import scripts, shared, images, scripts_postprocessing
from modules.processing import (
    Processed,
    StableDiffusionProcessing,
    StableDiffusionProcessingImg2Img,
)
from modules.face_restoration import FaceRestoration
from modules.images import save_image
try:
    from modules.paths_internal import models_path
except:
    try:
        from modules.paths import models_path
    except:
        model_path = os.path.abspath("models")

from scripts.rf_logger import logger
from scripts.rf_swapper import EnhancementOptions, swap_face, check_process_halt, reset_messaged
from scripts.rf_version import version_flag, app_title
from scripts.rf_console_log_patch import apply_logging_patch
from scripts.rf_helpers import make_grid, get_image_path


MODELS_PATH = None

def get_models():
    global MODELS_PATH
    models_path_init = os.path.join(models_path, "insightface/*")
    models = glob.glob(models_path_init)
    models = [x for x in models if x.endswith(".onnx") or x.endswith(".pth")]
    models_names = []
    for model in models:
        model_path = os.path.split(model)
        if MODELS_PATH is None:
            MODELS_PATH = model_path[0]
        model_name = model_path[1]
        models_names.append(model_name)
    return models_names


class FaceSwapScript(scripts.Script):
    def title(self):
        return f"{app_title}"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion(f"{app_title}", open=False):
            with gr.Tab("Main"):
                with gr.Column():
                    img = gr.Image(type="pil")
                    enable = gr.Checkbox(False, label="Enable", info=f"The Fast and Simple FaceSwap Extension - {version_flag}")
                    save_original = gr.Checkbox(False, label="Save Original", info="Save the original image(s) made before swapping; If you use \"img2img\" - this option will affect with \"Swap in generated\" only")
                    gr.Markdown("<br>")
                    gr.Markdown("Source Image (above):")
                    with gr.Row():
                        source_faces_index = gr.Textbox(
                            value="0",
                            placeholder="Which face(s) to use as Source (comma separated)",
                            label="Comma separated face number(s); Example: 0,2,1",
                        )
                        gender_source = gr.Radio(
                            ["No", "Female Only", "Male Only"],
                            value="No",
                            label="Gender Detection (Source)",
                            type="index",
                        )
                    gr.Markdown("<br>")
                    gr.Markdown("Target Image (result):")
                    with gr.Row():
                        faces_index = gr.Textbox(
                            value="0",
                            placeholder="Which face(s) to Swap into Target (comma separated)",
                            label="Comma separated face number(s); Example: 1,0,2",
                        )
                        gender_target = gr.Radio(
                            ["No", "Female Only", "Male Only"],
                            value="No",
                            label="Gender Detection (Target)",
                            type="index",
                        )
                    gr.Markdown("<br>")
                    with gr.Row():
                        face_restorer_name = gr.Radio(
                            label="Restore Face",
                            choices=["None"] + [x.name() for x in shared.face_restorers],
                            value=shared.face_restorers[0].name(),
                            type="value",
                        )
                        with gr.Column():
                            face_restorer_visibility = gr.Slider(
                                0, 1, 1, step=0.1, label="Restore Face Visibility"
                            )
                            codeformer_weight = gr.Slider(
                                0, 1, 0.5, step=0.1, label="CodeFormer Weight", info="0 = maximum effect, 1 = minimum effect"
                            )
                    gr.Markdown("<br>")
                    swap_in_source = gr.Checkbox(
                        False,
                        label="Swap in source image",
                        visible=is_img2img,
                    )
                    swap_in_generated = gr.Checkbox(
                        True,
                        label="Swap in generated image",
                        visible=is_img2img,
                    )                    
            with gr.Tab("Upscale"):
                restore_first = gr.Checkbox(
                    True,
                    label="1. Restore Face -> 2. Upscale (-Uncheck- if you want vice versa)",
                    info="Postprocessing Order"
                )
                upscaler_name = gr.Dropdown(
                    choices=[upscaler.name for upscaler in shared.sd_upscalers],
                    label="Upscaler",
                    value="None",
                    info="Won't scale if you choose -Swap in Source- via img2img, only 1x-postprocessing will affect (texturing, denoising, restyling etc.)"
                )
                gr.Markdown("<br>")
                with gr.Row():
                    upscaler_scale = gr.Slider(1, 8, 1, step=0.1, label="Scale by")
                    upscaler_visibility = gr.Slider(
                        0, 1, 1, step=0.1, label="Upscaler Visibility (if scale = 1)"
                    )
            with gr.Tab("Settings"):
                models = get_models()
                with gr.Row():
                    if len(models) == 0:
                        logger.warning(
                            "You should at least have one model in models directory, please read the doc here : https://github.com/Gourieff/sd-webui-reactor/"
                        )
                        model = gr.Dropdown(
                            choices=models,
                            label="Model not found, please download one and reload WebUI",
                        )
                    else:
                        model = gr.Dropdown(
                            choices=models, label="Model", value=models[0]
                        )
                    console_logging_level = gr.Radio(
                        ["No log", "Minimum", "Default"],
                        value="Minimum",
                        label="Console Log Level",
                        type="index",
                    )

        return [
            img,
            enable,
            source_faces_index,
            faces_index,
            model,
            face_restorer_name,
            face_restorer_visibility,
            restore_first,
            upscaler_name,
            upscaler_scale,
            upscaler_visibility,
            swap_in_source,
            swap_in_generated,
            console_logging_level,
            gender_source,
            gender_target,
            save_original,
            codeformer_weight,
        ]


    @property
    def upscaler(self) -> UpscalerData:
        for upscaler in shared.sd_upscalers:
            if upscaler.name == self.upscaler_name:
                return upscaler
        return None

    @property
    def face_restorer(self) -> FaceRestoration:
        for face_restorer in shared.face_restorers:
            if face_restorer.name() == self.face_restorer_name:
                return face_restorer
        return None

    @property
    def enhancement_options(self) -> EnhancementOptions:
        return EnhancementOptions(
            do_restore_first = self.restore_first,
            scale=self.upscaler_scale,
            upscaler=self.upscaler,
            face_restorer=self.face_restorer,
            upscale_visibility=self.upscaler_visibility,
            restorer_visibility=self.face_restorer_visibility,
            codeformer_weight=self.codeformer_weight,
        )

    def process(
        self,
        p: StableDiffusionProcessing,
        img,
        enable,
        source_faces_index,
        faces_index,
        model,
        face_restorer_name,
        face_restorer_visibility,
        restore_first,
        upscaler_name,
        upscaler_scale,
        upscaler_visibility,
        swap_in_source,
        swap_in_generated,
        console_logging_level,
        gender_source,
        gender_target,
        save_original,
        codeformer_weight,
    ):
        self.enable = enable
        if self.enable:

            reset_messaged()
            if check_process_halt():
                return
            
            global MODELS_PATH
            self.source = img
            self.face_restorer_name = face_restorer_name
            self.upscaler_scale = upscaler_scale
            self.upscaler_visibility = upscaler_visibility
            self.face_restorer_visibility = face_restorer_visibility
            self.restore_first = restore_first
            self.upscaler_name = upscaler_name       
            self.swap_in_generated = swap_in_generated
            self.model = os.path.join(MODELS_PATH,model)
            self.console_logging_level = console_logging_level
            self.gender_source = gender_source
            self.gender_target = gender_target
            self.save_original = save_original
            self.codeformer_weight = codeformer_weight
            if self.gender_source is None or self.gender_source == "No":
                self.gender_source = 0
            if self.gender_target is None or self.gender_target == "No":
                self.gender_target = 0
            self.source_faces_index = [
                int(x) for x in source_faces_index.strip(",").split(",") if x.isnumeric()
            ]
            self.faces_index = [
                int(x) for x in faces_index.strip(",").split(",") if x.isnumeric()
            ]
            if len(self.source_faces_index) == 0:
                self.source_faces_index = [0]
            if len(self.faces_index) == 0:
                self.faces_index = [0]
            if self.save_original is None:
                self.save_original = False

            if self.source is not None:
                apply_logging_patch(console_logging_level)
                if isinstance(p, StableDiffusionProcessingImg2Img) and swap_in_source:
                    logger.status("Working: source face index %s, target face index %s", self.source_faces_index, self.faces_index)

                    for i in range(len(p.init_images)):
                        if len(p.init_images) > 1:
                            logger.status("Swap in %s", i)
                        result, output, swapped = swap_face(
                            self.source,
                            p.init_images[i],
                            source_faces_index=self.source_faces_index,
                            faces_index=self.faces_index,
                            model=self.model,
                            enhancement_options=self.enhancement_options,
                            gender_source=self.gender_source,
                            gender_target=self.gender_target,
                        )
                        p.init_images[i] = result
                        # result_path = get_image_path(p.init_images[i], p.outpath_samples, "", p.all_seeds[i], p.all_prompts[i], "txt", p=p, suffix="-swapped")
                        # if len(output) != 0:
                        #     with open(result_path, 'w', encoding="utf8") as f:
                        #         f.writelines(output)

                        if shared.state.interrupted or shared.state.skipped:
                            return
            
            else:
                logger.error("Please provide a source face")

    def postprocess(self, p: StableDiffusionProcessing, processed: Processed, *args):
        if self.enable:

            reset_messaged()
            if check_process_halt():
                return

            if self.save_original:

                postprocess_run: bool = True

                orig_images : List[Image.Image] = processed.images[processed.index_of_first_image:]
                orig_infotexts : List[str] = processed.infotexts[processed.index_of_first_image:]

                result_images: List = processed.images
                # result_info: List = processed.infotexts

                if self.swap_in_generated:
                    logger.status("Working: source face index %s, target face index %s", self.source_faces_index, self.faces_index)
                    if self.source is not None:
                        for i,(img,info) in enumerate(zip(orig_images, orig_infotexts)):
                            if check_process_halt():
                                postprocess_run = False
                                break
                            if len(orig_images) > 1:
                                logger.status("Swap in %s", i)
                            result, output, swapped = swap_face(
                                self.source,
                                img,
                                source_faces_index=self.source_faces_index,
                                faces_index=self.faces_index,
                                model=self.model,
                                enhancement_options=self.enhancement_options,
                                gender_source=self.gender_source,
                                gender_target=self.gender_target,
                            )
                            if result is not None and swapped > 0:
                                result_images.append(result)
                                suffix = "-swapped"
                                try:
                                    img_path = save_image(result, p.outpath_samples, "", p.all_seeds[0], p.all_prompts[0], "png",info=info, p=p, suffix=suffix)
                                except:
                                    logger.error("Cannot save a result image - please, check SD WebUI Settings (Saving and Paths)")
                            elif result is None:
                                logger.error("Cannot create a result image")
                            
                            # if len(output) != 0:
                            #     split_fullfn = os.path.splitext(img_path[0])
                            #     fullfn = split_fullfn[0] + ".txt"
                            #     with open(fullfn, 'w', encoding="utf8") as f:
                            #         f.writelines(output)
                
                if shared.opts.return_grid and len(result_images) > 2 and postprocess_run:
                    grid = make_grid(result_images)
                    result_images.insert(0, grid)
                    try:
                        save_image(grid, p.outpath_grids, "grid", p.all_seeds[0], p.all_prompts[0], shared.opts.grid_format, info=info, short_filename=not shared.opts.grid_extended_filename, p=p, grid=True)
                    except:
                        logger.error("Cannot save a grid - please, check SD WebUI Settings (Saving and Paths)")
                
                processed.images = result_images
                # processed.infotexts = result_info
    
    def postprocess_batch(self, p, *args, **kwargs):
        if self.enable and not self.save_original:
            images = kwargs["images"]

    def postprocess_image(self, p, script_pp: scripts.PostprocessImageArgs, *args):
        if self.enable and self.swap_in_generated and not self.save_original:

            current_job_number = shared.state.job_no + 1
            job_count = shared.state.job_count
            if current_job_number == job_count:
                reset_messaged()
            if check_process_halt():
                return
            
            if self.source is not None:
                logger.status("Working: source face index %s, target face index %s", self.source_faces_index, self.faces_index)
                image: Image.Image = script_pp.image
                result, output, swapped = swap_face(
                    self.source,
                    image,
                    source_faces_index=self.source_faces_index,
                    faces_index=self.faces_index,
                    model=self.model,
                    enhancement_options=self.enhancement_options,
                    gender_source=self.gender_source,
                    gender_target=self.gender_target,
                )
                try:
                    pp = scripts_postprocessing.PostprocessedImage(result)
                    pp.info = {}
                    p.extra_generation_params.update(pp.info)
                    script_pp.image = pp.image

                    # if len(output) != 0:
                    #     result_path = get_image_path(script_pp.image, p.outpath_samples, "", p.all_seeds[0], p.all_prompts[0], "txt", p=p, suffix="-swapped")
                    #     if len(output) != 0:
                    #         with open(result_path, 'w', encoding="utf8") as f:
                    #             f.writelines(output)
                except:
                    logger.error("Cannot create a result image")
