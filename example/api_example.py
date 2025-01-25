import base64, io, requests, json
from PIL import Image, PngImagePlugin
from datetime import datetime, date

address = 'http://127.0.0.1:7860'
input_file = "extensions\sd-webui-reactor\example\IamSFW.jpg" # Input file path
time = datetime.now()
today = date.today()
current_date = today.strftime('%Y-%m-%d')
current_time = time.strftime('%H-%M-%S')
output = 'outputs/api/output_'+current_date+'_'+current_time # Output file path + name index
try:
    im = Image.open(input_file)
except Exception as e:
    print(e)
finally:
    print(im)

img_bytes = io.BytesIO()
im.save(img_bytes, format='PNG')
img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

# ReActor arguments:
args=[
    img_base64, #0
    True, #1 Enable ReActor
    '0', #2 Comma separated face number(s) from swap-source image
    '0', #3 Comma separated face number(s) for target image (result)
    'C:\stable-diffusion-webui\models\insightface\inswapper_128.onnx', #4 model path
    'CodeFormer', #4 Restore Face: None; CodeFormer; GFPGAN
    1, #5 Restore visibility value
    True, #7 Restore face -> Upscale
    '4x_NMKD-Superscale-SP_178000_G', #8 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> reactor -> sec.8
    1.5, #9 Upscaler scale value
    1, #10 Upscaler visibility (if scale = 1)
    False, #11 Swap in source image
    True, #12 Swap in generated image
    1, #13 Console Log Level (0 - min, 1 - med or 2 - max)
    0, #14 Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)
    0, #15 Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)
    False, #16 Save the original image(s) made before swapping
    0.8, #17 CodeFormer Weight (0 = maximum effect, 1 = minimum effect), 0.5 - by default
    False, #18 Source Image Hash Check, True - by default
    False, #19 Target Image Hash Check, False - by default
    "CUDA", #20 CPU or CUDA (if you have it), CPU - by default
    True, #21 Face Mask Correction
    1, #22 Select Source, 0 - Image, 1 - Face Model, 2 - Source Folder
    "elena.safetensors", #23 Filename of the face model (from "models/reactor/faces"), e.g. elena.safetensors, don't forger to set #22 to 1
    "C:\PATH_TO_FACES_IMAGES", #24 The path to the folder containing source faces images, don't forger to set #22 to 2
    None, #25 skip it for API
    True, #26 Randomly select an image from the path
    True, #27 Force Upscale even if no face found
    0.6, #28 Face Detection Threshold
    2, #29 Maximum number of faces to detect (0 is unlimited)
]

# The args for ReActor can be found by 
# requests.get(url=f'{address}/sdapi/v1/script-info')

prompt = "(8k, best quality, masterpiece, highly detailed:1.1),realistic photo of fantastic happy woman,hairstyle of blonde and red short bob hair,modern clothing,cinematic lightning,film grain,dynamic pose,bokeh,dof"

neg = "ng_deepnegative_v1_75t,(badhandv4:1.2),(worst quality:2),(low quality:2),(normal quality:2),lowres,(bad anatomy),(bad hands),((monochrome)),((grayscale)),(verybadimagenegative_v1.3:0.8),negative_hand-neg,badhandv4,nude,naked,(strabismus),cross-eye,heterochromia,((blurred))"

payload = {
    "prompt": prompt,
    "negative_prompt": neg,
    "seed": -1,
    "sampler_name": "DPM++ 2M Karras",
    "steps": 15,
    "cfg_scale": 7,
    "width": 512,
    "height": 768,
    "restore_faces": False,
    "alwayson_scripts": {"reactor":{"args":args}}
}

try:
    print('Working... Please wait...')
    result = requests.post(url=f'{address}/sdapi/v1/txt2img', json=payload)
except Exception as e:
    print(e)
finally:
    print('Done! Saving file...')

if result is not None:
    r = result.json()
    n = 0

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{address}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        output_file = output+'_'+str(n)+'_.png'
        try:
            image.save(output_file, pnginfo=pnginfo)
        except Exception as e:
            print(e)
        finally:
            print(f'{output_file} is saved\nAll is done!')
        n += 1
else:
    print('Something went wrong...')
