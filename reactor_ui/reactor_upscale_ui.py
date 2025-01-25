import gradio as gr
from modules import shared

def update_upscalers_list(selected: str):
    return gr.Dropdown.update(
        value=selected, choices=[upscaler.name for upscaler in shared.sd_upscalers]
    )

# TAB UPSCALE
def show(show_br: bool = True):
    with gr.Tab("Upscale"):
        with gr.Row():
            restore_first = gr.Checkbox(
                True,
                label="1. Restore Face -> 2. Upscale (-Uncheck- if you want vice versa)",
                info="Postprocessing Order",
                scale=2
            )
            upscale_force = gr.Checkbox(
                False,
                label="Force Upscale",
                info="Upscale anyway - even if no face found",
                scale=1
            )
        with gr.Row():
            upscaler_name = gr.Dropdown(
                choices=[upscaler.name for upscaler in shared.sd_upscalers],
                label="Upscaler",
                value="None",
                info="Won't scale if you choose -Swap in Source- via img2img, only 1x-postprocessing will affect (texturing, denoising, restyling etc.)"
            )
            upscalers_update = gr.Button(
                value="🔄",
                variant="tool",
            )
        upscalers_update.click(
            update_upscalers_list, 
            inputs=[upscaler_name],
            outputs=[upscaler_name],
        )
        gr.Markdown("<br>", visible=show_br)
        with gr.Row():
            upscaler_scale = gr.Slider(1, 8, 1, step=0.1, label="Scale by")
            upscaler_visibility = gr.Slider(
                0, 1, 1, step=0.1, label="Upscaler Visibility (if scale = 1)"
            )
    return restore_first, upscaler_name, upscaler_scale, upscaler_visibility, upscale_force
