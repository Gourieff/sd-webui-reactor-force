import gradio as gr
from scripts.reactor_helpers import (
    get_model_names, 
    get_facemodels
)
from scripts.reactor_swapper import (
    clear_faces_list,
)
from modules import shared

# SAVE_ORIGINAL: bool = False

def update_fm_list(selected: str):
    try: # GR3.x
        return gr.Dropdown.update(
            value=selected, choices=get_model_names(get_facemodels)
        )
    except: # GR4.x
        return gr.Dropdown(
            value=selected, choices=get_model_names(get_facemodels)
        )

# TAB MAIN
def show(is_img2img: bool, show_br: bool = True, **msgs):

    # def on_select_source(selected: bool, evt: gr.SelectData):
    def on_select_source(evt: gr.SelectData):
        # global SAVE_ORIGINAL
        if evt.index == 2:
            # if SAVE_ORIGINAL != selected:
            #     SAVE_ORIGINAL = selected
            try: # GR3.x
                return {
                    control_col_1: gr.Column.update(visible=False),
                    control_col_2: gr.Column.update(visible=False),
                    control_col_3: gr.Column.update(visible=True),
                    # save_original: gr.Checkbox.update(value=False,visible=False),
                    imgs_hash_clear: gr.Button.update(visible=True)
                }
            except: # GR4.x
                return {
                    control_col_1: gr.Column(visible=False),
                    control_col_2: gr.Column(visible=False),
                    control_col_3: gr.Column(visible=True),
                    # save_original: gr.Checkbox.update(value=False,visible=False),
                    imgs_hash_clear: gr.Button(visible=True)
                }
        if evt.index == 0:
            try: # GR3.x
                return {
                    control_col_1: gr.Column.update(visible=True),
                    control_col_2: gr.Column.update(visible=False),
                    control_col_3: gr.Column.update(visible=False),
                    # save_original: gr.Checkbox.update(value=SAVE_ORIGINAL,visible=show_br),
                    imgs_hash_clear: gr.Button.update(visible=False)
                }
            except: # GR4.x
                return {
                    control_col_1: gr.Column(visible=True),
                    control_col_2: gr.Column(visible=False),
                    control_col_3: gr.Column(visible=False),
                    # save_original: gr.Checkbox.update(value=SAVE_ORIGINAL,visible=show_br),
                    imgs_hash_clear: gr.Button(visible=False)
                }
        if evt.index == 1:
            try: # GR3.x
                return {
                    control_col_1: gr.Column.update(visible=False),
                    control_col_2: gr.Column.update(visible=True),
                    control_col_3: gr.Column.update(visible=False),
                    # save_original: gr.Checkbox.update(value=SAVE_ORIGINAL,visible=show_br),
                    imgs_hash_clear: gr.Button.update(visible=False)
                }
            except: # GR4.x
                return {
                    control_col_1: gr.Column(visible=False),
                    control_col_2: gr.Column(visible=True),
                    control_col_3: gr.Column(visible=False),
                    # save_original: gr.Checkbox.update(value=SAVE_ORIGINAL,visible=show_br),
                    imgs_hash_clear: gr.Button(visible=False)
                }
        
    progressbar_area = gr.Markdown("")
    with gr.Tab("Main"):
        with gr.Column():
            with gr.Row():
                select_source = gr.Radio(
                    ["Image(s)","Face Model","Folder"],
                    value="Image(s)",
                    label="Select Source",
                    type="index",
                    scale=1,
                )
                with gr.Column(visible=False) as control_col_2:
                    with gr.Row():
                        face_models = get_model_names(get_facemodels)
                        face_model = gr.Dropdown(
                            choices=face_models,
                            label="Choose Face Model",
                            value="None",
                            scale=1,
                        )
                        fm_update = gr.Button(
                            value="🔄",
                            variant="tool",
                        )
                        fm_update.click(
                            update_fm_list, 
                            inputs=[face_model],
                            outputs=[face_model],
                        )
                imgs_hash_clear = gr.Button(
                    value="Clear Source Images Hash",
                    scale=1,
                    visible=False,
                )
                imgs_hash_clear.click(clear_faces_list,None,[progressbar_area])
            gr.Markdown("<br>", visible=show_br)
            with gr.Column(visible=True) as control_col_1:
                with gr.Row():
                    selected_tab = gr.Textbox('tab_single', visible=False)
                    with gr.Tabs() as tab_single:
                        with gr.Tab('Single'):
                            img = gr.Image(
                                type="pil",
                                label="Single Source Image",
                            )
                        with gr.Tab('Multiple') as tab_multiple:
                            imgs = gr.Files(
                                label=f"Multiple Source Images{msgs['extra_multiple_source']}",
                                file_types=["image"],
                            )
                    tab_single.select(fn=lambda: 'tab_single', inputs=[], outputs=[selected_tab])
                    tab_multiple.select(fn=lambda: 'tab_multiple', inputs=[], outputs=[selected_tab])
            with gr.Column(visible=False) as control_col_3:
                gr.Markdown("<span style='display:block;text-align:right;padding-right:3px;margin: -15px 0;font-size:1.1em'><sup>Clear Hash if you see the previous face was swapped instead of the new one</sup></span>")
                with gr.Row():
                    source_folder = gr.Textbox(
                        value="",
                        placeholder="Paste here the path to the folder containing source faces images",
                        label=f"Source Folder{msgs['extra_multiple_source']}",
                        scale=2,
                    )
                    random_image = gr.Checkbox(
                        False,
                        label="Random Image",
                        info="Randomly select an image from the path",
                        scale=1,
                    )
            setattr(face_model, "do_not_save_to_config", True)
            if is_img2img:
                save_original = gr.Checkbox(
                    False,
                    label="Save Original (Swap in generated only)", 
                    info="Save the original image(s) made before swapping"
                )
            else:
                save_original = gr.Checkbox(
                    False,
                    label="Save Original", 
                    info="Save the original image(s) made before swapping",
                    visible=show_br
                )
            # imgs.upload(on_files_upload_uncheck_so,[save_original],[save_original],show_progress=False)
            # imgs.clear(on_files_clear,None,[save_original],show_progress=False)
            imgs.clear(clear_faces_list,None,None,show_progress=False)
            mask_face = gr.Checkbox(
                False,
                label="Face Mask Correction", 
                info="Apply this option if you see some pixelation around face contours"
            )
            gr.Markdown("<br>", visible=show_br)
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
            gr.Markdown("<br>", visible=show_br)
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
            gr.Markdown("<br>", visible=show_br)
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
                        0, 1, 0.5, step=0.1, label="CodeFormer Weight (Fidelity)", info="0 = far from original (max restoration), 1 = close to original (min restoration)"
                    )
            gr.Markdown("<br>", visible=show_br)
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
    # select_source.select(on_select_source,[save_original],[control_col_1,control_col_2,control_col_3,save_original,imgs_hash_clear],show_progress=False)
    select_source.select(on_select_source,None,[control_col_1,control_col_2,control_col_3,imgs_hash_clear],show_progress=False)

    return img, imgs, selected_tab, select_source, face_model, source_folder, save_original, mask_face, source_faces_index, gender_source, faces_index, gender_target, face_restorer_name, face_restorer_visibility, codeformer_weight, swap_in_source, swap_in_generated, random_image
