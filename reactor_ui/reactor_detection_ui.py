import gradio as gr
from scripts.reactor_swapper import (
    clear_faces,
    clear_faces_list,
    clear_faces_target,
    clear_faces_all
)

# TAB DETECTION
def show(show_br: bool = True):
    with gr.Tab("Detection"):
        with gr.Row():
            det_thresh = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.5,
                step=0.01,
                label="Threshold",
                info="The higher the value, the more sensitive the detection is to what is considered a face (0.5 by default)",
                scale=2
            )
            det_maxnum = gr.Slider(
                minimum=0,
                maximum=20,
                value=0,
                step=1,
                label="Max Faces",
                info="Maximum number of faces to detect (0 is unlimited)",
                scale=1
            )
        # gr.Markdown("<br>", visible=show_br)
        gr.Markdown("Hashed images get processed with previously set detection parameters (the face is hashed with all available parameters to bypass the analyzer and speed up the process). Please clear the hash if you want to apply new detection settings.", visible=show_br)
        with gr.Row():
            imgs_hash_clear_single = gr.Button(
                value="Clear Source Images Hash (Single)",
                scale=1
            )
            imgs_hash_clear_multiple = gr.Button(
                value="Clear Source Images Hash (Multiple)",
                scale=1
            )
            imgs_hash_clear_target = gr.Button(
                value="Clear Target Image Hash",
                scale=1
            )
            imgs_hash_clear_all = gr.Button(
                value="Clear All Hash"
            )
        progressbar_area = gr.Markdown("")
        imgs_hash_clear_single.click(clear_faces,None,[progressbar_area])
        imgs_hash_clear_multiple.click(clear_faces_list,None,[progressbar_area])
        imgs_hash_clear_target.click(clear_faces_target,None,[progressbar_area])
        imgs_hash_clear_all.click(clear_faces_all,None,[progressbar_area])
    return det_thresh, det_maxnum
