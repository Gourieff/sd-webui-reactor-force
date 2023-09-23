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
    "upscaler": "4x_Struzan_300000",
    "scale": 2,
    "upscale_visibility": 1,
    "face_restorer": "CodeFormer",
    "restorer_visibility": 1,
    "restore_first": 1,
    "model": "inswapper_128.onnx",
    "gender_source": 0,
    "gender_target": 0,
    "save_to_file": 0,
    "result_file_path": ""
	}'
```

* Set `"upscaler"` to `"None"` and `"scale"` to `1` if you don't need to upscale;
* Set `"save_to_file"` to `1` if you need to save result to a file;
* `"result_file_path"` is set to the `"outputs/api"` folder by default (please, create the folder beforehand to avoid any errors) with a timestamped filename; (output_YYYY-MM-DD_hh-mm-ss), you can set any specific path, e.g. `"C:/stable-diffusion-webui/outputs/api/output.png"`.

You can find full usage examples with all the available parameters in the "example" folder: [cURL](./example/api_external.curl), [JSON](./example/api_external.json).

As a result you recieve a "base64" image:

```
{"image":"iVBORw0KGgoAAAANSUhEUgAABlAAAARQCAIAAAAdiYuqAAEAAElEQVR4nOz9+ZMlSXImBn6qau4vIjKzzr5wzwBCDrm/7f+/K7IHV3ZkhUIuyZHlkBhiMGig0Y0..."}
```

A list of available models can be seen by GET:
* http://127.0.0.1:7860/reactor/models
* http://127.0.0.1:7860/reactor/upscalers
