# <div align="center">ReActor Extension API</div>

<div align="center">

[Built-in SD WebUI API](#built-in-sd-webui-api) | [External ReActor API](#external-reactor-api)

---
</div>

Gourieff's **ReActor** SD WebUI Extension allows to operate via API: both built-in and external (POST and GET requests).


## Built-in SD WebUI API

This API is actual if you use Automatic1111 stable-diffusion-webui.

First of all - check the [SD Web API Wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API) for how to use the API.

* Call `requests.get(url=f'{address}/sdapi/v1/script-info')` to find the args that ReActor needs;
* Define ReActor script args and add like this `"alwayson_scripts": {"reactor":{"args":args}}` in the payload;
* Call the API. 

You can find the [full usage example](./example/api_example.py) with all the available parameters and discriptions in the "example" folder.

## External ReActor API

ReActor extension supports for external calls via POST or GET requests while your SD WebUI server is working.

> :warning: Source and Target images must be "base64".

Example:

```
curl -X POST \
	'http://127.0.0.1:7860/reactor/image' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "source_image": "data:image/png;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/7g...",
    "target_image": "data:image/png;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABCAAD/7g...",
    "source_faces_index": [0],
    "face_index": [0],
    "upscaler": "4x_NMKD-Siax_200k",
    "scale": 2,
    "upscale_visibility": 1,
    "face_restorer": "CodeFormer",
    "restorer_visibility": 1,
    "restore_first": 1,
    "model": "inswapper_128.onnx",
    "gender_source": 0,
    "gender_target": 0,
    "save_to_file": 0,
    "result_file_path": "",
    "device": "CUDA",
    "mask_face": 1,
    "select_source": 1,
    "face_model": "elena.safetensors",
    "source_folder": "C:/faces",
    "random_image": 1,
    "upscale_force": 1
	}'
```

* Set `"upscaler"` to `"None"` and `"scale"` to `1` if you don't need to upscale;
* Set `"save_to_file"` to `1` if you need to save result to a file;
* `"result_file_path"` is set to the `"outputs/api"` folder by default (please, create the folder beforehand to avoid any errors) with a timestamped filename; (output_YYYY-MM-DD_hh-mm-ss), you can set any specific path, e.g. `"C:/stable-diffusion-webui/outputs/api/output.png"`;
* Set `"mask_face"` to `1` if you want ReActor to mask the face or to `0` if want ReActor to create a bbox around the face;
* Set `"select_source"` to: 0 - Image, 1 - Face Model, 2 - Source Folder;
* Set `"face_model"` to the face model file you want to choose if you set `"select_source": 1`;
* Set `"source_folder"` to the path with source images (with faces you need as the results) if you set `"select_source": 2`;
* Set `"random_image"` to `1` if want ReActor to choose a random image from the path of `"source_folder"`;
* Set `"upscale_force"` to `1` if you want ReActor to upscale the image even if no face found.

You can find full usage examples with all the available parameters in the "example" folder: [cURL](./example/api_external.curl), [JSON](./example/api_external.json).

As a result you recieve a "base64" image:

```
{"image":"iVBORw0KGgoAAAANSUhEUgAABlAAAARQCAIAAAAdiYuqAAEAAElEQVR4nOz9+ZMlSXImBn6qau4vIjKzzr5wzwBCDrm/7f+/K7IHV3ZkhUIuyZHlkBhiMGig0Y0..."}
```

A list of available models can be seen by GET:
* http://127.0.0.1:7860/reactor/models
* http://127.0.0.1:7860/reactor/upscalers
* http://127.0.0.1:7860/reactor/facemodels

### FaceModel Buid API

Send POST to http://127.0.0.1:7860/reactor/facemodels with body:

```
{
    "source_images": ["data:image/png;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/7g...","data:image/png;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/7g...","data:image/png;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/7g..."],
    "name": "my_super_model",
    "compute_method": 0
}
```

where:<br>
"source_images" is a list of base64 encoded images,<br>
"compute_method" is: 0 - Mean, 1- Median, 2 - Mode
