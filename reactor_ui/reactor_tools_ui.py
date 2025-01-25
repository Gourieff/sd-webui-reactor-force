import gradio as gr
from scripts.reactor_swapper import build_face_model, blend_faces

# TAB TOOLS
def show():
    with gr.Tab("Tools"):
        with gr.Tab("Face Models"):

            with gr.Tab("Single"):
                gr.Markdown("Load an image containing one person, name it and click 'Build and Save'")
                img_fm = gr.Image(
                    type="pil",
                    label="Load an Image to build -Face Model-",
                )
                with gr.Row(equal_height=True):
                    fm_name = gr.Textbox(
                        value="",
                        placeholder="Please type any name (e.g. Elena)",
                        label="Face Model Name",
                    )
                    save_fm_btn = gr.Button("Build and Save")
                save_fm = gr.Markdown("You can find saved models in 'models/reactor/faces'")
                save_fm_btn.click(
                    build_face_model,
                    inputs=[img_fm, fm_name],
                    outputs=[save_fm],
                )
            
            with gr.Tab("Blend"):
                gr.Markdown("Load a set of images containing any person, name it and click 'Build and Save'")
                with gr.Row():
                    imgs_fm = gr.Files(
                        label=f"Load Images to build -Blended Face Model-",
                        file_types=["image"]
                    )
                    with gr.Column():
                        compute_method = gr.Radio(
                            ["Mean", "Median", "Mode"],
                            value="Mean",
                            label="Compute Method",
                            type="index",
                            info="Mean (recommended) - Average value (best result 👍); Median* - Mid-point value (may be funny 😅); Mode - Most common value (may be scary 😨); *Mean and Median will be similar if you load two images"
                        )
                        shape_check = gr.Checkbox(
                            False,
                            label="Check -Embedding Shape- on Similarity",
                            info="(Experimental) Turn it ON if you want to skip the faces which are too much different from the first one in the list to prevent some probable 'shape mismatches'"
                        )
                with gr.Row(equal_height=True):
                    fm_name = gr.Textbox(
                        value="",
                        placeholder="Please type any name (e.g. Elena)",
                        label="Face Model Name",
                    )
                    save_fm_btn = gr.Button("Build and Save")
                save_fm = gr.Markdown("You can find saved models in 'models/reactor/faces'")
                save_fm_btn.click(
                    blend_faces,
                    inputs=[imgs_fm, fm_name, compute_method, shape_check],
                    outputs=[save_fm],
                )
