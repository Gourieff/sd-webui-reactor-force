<div align="center">

  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/ReActor_logo_NEW_EN.png?raw=true" alt="logo" width="180px"/>
    
  ![Version](https://img.shields.io/badge/version-0.7.1_beta3-green?style=for-the-badge&labelColor=darkgreen)
  
  <a href="https://boosty.to/artgourieff" target="_blank">
    <img src="https://lovemet.ru/img/boosty.jpg" width="108" alt="Support Me on Boosty"/>
    <br>
    <sup>
      Support This Project
    </sup>
  </a>

  <hr>
  
  [![Commit activity](https://img.shields.io/github/commit-activity/t/Gourieff/sd-webui-reactor-sfw/main?cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-sfw/commits/main)
  ![Last commit](https://img.shields.io/github/last-commit/Gourieff/sd-webui-reactor-sfw/main?cacheSeconds=0)
  [![Opened issues](https://img.shields.io/github/issues/Gourieff/sd-webui-reactor-sfw?color=red)](https://github.com/Gourieff/sd-webui-reactor-sfw/issues?cacheSeconds=0)
  [![Closed issues](https://img.shields.io/github/issues-closed/Gourieff/sd-webui-reactor-sfw?color=green&cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-sfw/issues?q=is%3Aissue+is%3Aclosed)
  ![License](https://img.shields.io/github/license/Gourieff/sd-webui-reactor-sfw)

  English | [Русский](/README_RU.md)

# ReActor for Stable Diffusion

### The Fast and Simple FaceSwap Extension with a lot of improvements and with SFW filter (it has a nudity detector to avoid using this software with 18+ content)

> By using this Node you accept and assume [responsibility](#disclaimer)) 

---
  <b>
    <a href="#latestupdate">What's new</a> | <a href="#installation">Installation</a> | <a href="#features">Features</a> | <a href="#usage">Usage</a> | <a href="#api">API</a> | <a href="#troubleshooting">Troubleshooting</a> | <a href="#updating">Updating</a> | <a href="#comfyui">ComfyUI</a> | <a href="#disclaimer">Disclaimer</a>
  </b>
</div>

---

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/demo_crop.jpg?raw=true" alt="example"/>

<a name="latestupdate">

## What's new in the latest updates

### 0.7.1 <sub><sup>BETA1

- Allow spaces for face indexes (e.g.: 0, 1, 2)
- Sorting of face models list alphabetically
- [FaceModels Build API](./API.md#facemodel-build-api)
- Fixes and improvements

<details>
	<summary><a>Click to expand more</a></summary>

### 0.7.0 <sub><sup>BETA2

- X/Y/Z is improved! One more parameter is ready: you can now select several face models to create a variation of swaps to choose the best one!

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-05.jpg?raw=true" alt="0.7.0-whatsnew-05" width="100%"/>

To use "Face Model" axis - you should enable ReActor and choose any face model as the Source:<br>
<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-07.jpg?raw=true" alt="0.7.0-whatsnew-07" width="50%"/><img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-06.jpg?raw=true" alt="0.7.0-whatsnew-06" width="50%"/>

Full size demo image: [xyz_demo_2.png](https://raw.githubusercontent.com/Gourieff/Assets/main/sd-webui-reactor/xyz_demo_2.png)

### 0.7.0 <sub><sup>BETA1

- X/Y/Z Script support (up to 3 axes: CodeFormer Weight, Restorer Visibility, Face Mask Correction)

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-03.jpg?raw=true" alt="0.7.0-whatsnew-03" width="100%"/>

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-04.jpg?raw=true" alt="0.7.0-whatsnew-04" width="100%"/>

Full size demo image: [xyz_demo.png](https://raw.githubusercontent.com/Gourieff/Assets/main/sd-webui-reactor/xyz_demo.png)

__Don't forget to enable ReActor and set any source (to prevent "no source" error)__

### 0.7.0 <sub><sup>ALPHA1

- You can now blend faces to build blended face models ("Tools->Face Models->Blend") - due to popular demand

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-01.jpg?raw=true" alt="0.7.0-whatsnew-01" width="100%"/><img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-02.jpg?raw=true" alt="0.7.0-whatsnew-02" width="100%"/>

- CUDA 12 Support in the Installer script for 1.17.0 ORT-GPU library
- New tab "Detection" with "Threshold" and "Max Faces" parameters

### 0.6.1 <sub><sup>BETA3

- 'Force Upscale' option inside the 'Upscale' tab: ReActor will run the Upscaler even if there's no face is detected (FR https://github.com/Gourieff/sd-webui-reactor/issues/116)
- ReActor shows filenames of source images in-process when the multiple images mode or the folder mode (random as well) is selected

### 0.6.1 <sub><sup>BETA2

- 'Save original' option works fine now when you select 'Multiple Images' or 'Source Folder'
- Random Mode for 'Source Folder'

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/random_from_folder_demo_01.jpg?raw=true" alt="0.6.1-whatsnew-01" width="100%"/>

### 0.6.0

- New Logo
- Adaptation to A1111 1.7.0 (appropriate GFPGAN loader)
- New URL for the main model file
- UI reworked
- You can now load several source images (with reference faces) or set the path to the folder containing faces images

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/multiple_source_images_demo_01.png?raw=true" alt="0.6.0-whatsnew-01" width="100%"/>

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/multiple_source_images_demo_02.png?raw=true" alt="0.6.0-whatsnew-02" width="100%"/>

### 0.5.1

- You can save face models as "safetensors" files (stored in `<sd-web-ui-folder>\models\reactor\faces`) and load them into ReActor, keeping super lightweight face models of the faces you use;
- "Face Mask Correction" option - if you encounter some pixelation around face contours, this option will be useful;

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/face_model_demo_01.jpg?raw=true" alt="0.5.0-whatsnew-01" width="100%"/>

</details>

## Installation

[A1111 WebUI / WebUI-Forge](#a1111) | [SD.Next](#sdnext) | [Google Colab SD WebUI](#colab)

<a name="a1111">If you use [AUTOMATIC1111 SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui/) or [SD WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge):

1. (For Windows Users):
  - Install **Visual Studio 2022** (Community version, for example - you need this step to build some of dependencies):
  https://visualstudio.microsoft.com/downloads/
  - OR only **VS C++ Build Tools** (if you don't need the whole Visual Studio) and select "Desktop Development with C++" under "Workloads -> Desktop & Mobile":
  https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - OR if you don't want to install VS or VS C++ BT - follow [this steps (sec. VIII)](#insightfacebuild)
2. In web-ui, go to the "Extensions" tab, load "Available" extensions and type "ReActor" in the search field or use this URL `https://github.com/Gourieff/sd-webui-reactor-sfw` in the "Install from URL" tab - and click "Install"
3. Please, wait for several minutes until the installation process will be finished (be patient, don't interrupt the process)
4. Check the last message in your SD-WebUI Console:
* If you see the message "--- PLEASE, RESTART the Server! ---" - so, do it, stop the Server (CTRL+C or CMD+C) and start it again - or just go to the "Installed" tab, click "Apply and restart UI" 
* If you see the message "Done!", just reload the UI
5. Enjoy!

<a name="sdnext">If you use [SD.Next](https://github.com/vladmandic/automatic):

1. Close (stop) your SD WebUI Server if it's running
2. (For Windows Users) See the [1st step](#a1111) for Automatic1111 (if you followed [this steps (sec. VIII)](#insightfacebuild) instead - go to the Step 5)
3. Go to (Windows)`automatic\venv\Scripts` or (MacOS/Linux)`automatic/venv/bin`, run Terminal or Console (cmd) for that folder and type `activate`
4. Run `pip install insightface==0.7.3`
5. Run SD.Next, go to the "Extensions" tab and use this URL `https://github.com/Gourieff/sd-webui-reactor-sfw` in the "Install from URL" tab and click "Install"
6. Please, wait for several minutes until the installation process will be finished (be patient, don't interrupt the process)
7. Check the last message in your SD.Next Console:
* If you see the message "--- PLEASE, RESTART the Server! ---" - stop the Server (CTRL+C or CMD+C) or just close your console
8. Go to the `automatic\extensions\sd-webui-reactor-sfw` directory - if you see there `models\insightface` folder with the file `inswapper_128.onnx`, just move the file to the `automatic\models\insightface` folder
9. Run your SD.Next WebUI and enjoy!

<a name="colab">If you use [Cagliostro Colab UI](https://github.com/Linaqruf/sd-notebook-collection):

1. In active WebUI, go to the "Extensions" tab, load "Available" extensions and type "ReActor" in the search field or use this URL `https://github.com/Gourieff/sd-webui-reactor-sfw` in the "Install from URL" tab - and click "Install"
2. Please, wait for several minutes until the installation process will be finished (be patient, don't interrupt the process)
3. When you see the message "--- PLEASE, RESTART the Server! ---" (in your Colab Notebook Start UI section "Start Cagliostro Colab UI") - just go to the "Installed" tab and click "Apply and restart UI"
4. Enjoy!

## Features

- Very fast and accurate **face replacement (face swap)** in images
- **Multiple faces support**
- **Gender detection**
- Ability to **save original images** (made before swapping)
- **Face restoration** of a swapped face
- **Upscaling** of a resulting image
- Saving ans loading **Safetensors Face Models**
- **Facial Mask Correction** to avoid any  pixelation around face contours
- Ability to set the **Postprocessing order**
- **100% compatibility** with different **SD WebUIs**: Automatic1111, SD.Next, Cagliostro Colab UI
- **Fast performance** even with CPU, ReActor for SD WebUI is absolutely not picky about how powerful your GPU is
- **CUDA** acceleration support since version 0.5.0
- **[API](/API.md) support**: both SD WebUI built-in and external (via POST/GET requests)
- **ComfyUI [support](https://github.com/Gourieff/ComfyUI-ReActor)**
- **Mac M1/M2 [support](https://github.com/Gourieff/sd-webui-reactor/issues/42)**
- Console **log level control**
- **NSFW filter free** (this extension is aimed at highly developed intellectual people, not at perverts; our society must be oriented on its way towards the highest standards, not the lowest - this is the essence of development and evolution; so, my position is - that mature-minded people are clever enough to understand for themselves what is good and what is bad and take full responsibility for personal actions; for others - no "filters" will help until they do understand how Universe works)

## Usage

> Using this software you are agree with [disclaimer](#disclaimer)

1. Under "ReActor" drop-down menu, import an image containing a face;
2. Turn on the "Enable" checkbox;
3. That's it, now the generated result will have the face you selected.

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/example.jpg?raw=true" alt="example" width="808"/>

### Face Indexes

ReActor detects faces in images in the following order:<br>
left->right, top->bottom

And if you need to specify faces, you can set indexes for source and input images.

Index of the first detected face is 0.

You can set indexes in the order you need.<br>
E.g.: 0,1,2 (for Source); 1,0,2 (for Input).<br>
This means: the second Input face (index = 1) will be swapped by the first Source face (index = 0) and so on.

### Genders

You can specify the gender to detect in images.<br>
ReActor will swap a face only if it meets the given condition.

### The result face is blurry
Use the "Restore Face" option. You can also try the "Upscaler" option or for more finer control, use an upscaler from the "Extras" tab.
You can also set the postproduction order (from 0.1.0 version):
<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/pp-order.png?raw=true" alt="example"/>

*The old logic was the opposite (Upscale -> then Restore), resulting in worse face quality (and big texture differences) after upscaling.* 

### There are multiple faces in result
Select the face numbers you wish to swap using the "Comma separated face number(s)" option for swap-source and result images. You can use different index order.
<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/multiple-faces.png?raw=true" alt="example"/>

### Img2Img

You can choose to activate the swap on the source image or on the generated image, or on both using the checkboxes. Activating on source image allows you to start from a given base and apply the diffusion process to it.

ReActor works with Inpainting - but only the masked part will be swapped.<br>Please use with the "Only masked" option for "Inpaint area" if you enabled "Upscaler". Otherwise use the upscale option via the Extras tab or via the Script loader (below the screen) with "SD upscale" or "Ultimate SD upscale".

### Extras Tab

From the version 0.5.0 you can use ReActor via the Extras Tab. It gives a superfast perfomance and ability to swap face2image avoiding SD pipeline that can cause smushing of original image's details

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/extras_tab.jpg?raw=true" alt="IamSFW"/>

## API

You can use ReActor with the built-in Webui API or via an external API.

Please follow **[this](/API.md)** page for the detailed instruction.

## Troubleshooting

### **I. "You should at least have one model in models directory"**

Please, check the path where "inswapper_128.onnx" model is stored. It must be inside the folder `stable-diffusion-webui\models\insightface`. Move the model there if it's stored in a different directory.

### **II. Any problems with installing Insightface or other dependencies**

(for Mac M1/M2 users) If you get errors when trying to install Insightface - please read https://github.com/Gourieff/sd-webui-reactor/issues/42

(for Windows Users) If you have VS C++ Build Tools or MS VS 2022 installed but still have a problem, then try the next step:
1. Close (stop) your SD WebUI Server and start it again
   
(for Any OS Users) If the problem still there, then do the following:
1. Close (stop) your SD WebUI Server if it's running
2. Go to (Windows)`venv\Lib\site-packages` folder or (MacOS/Linux)`venv/lib/python3.10/site-packages`
3. If you see any folders with names start from `~` (e.g. "~rotobuf") - delete them
4. Go to (Windows)`venv\Scripts` or (MacOS/Linux)`venv/bin`
5. Run Terminal or Console (cmd) for that folder and type `activate`
6. Update your pip at first: `pip install -U pip`
7. Then one-by-one:
   - `pip install insightface==0.7.3`
   - `pip install onnx`
   - `pip install "onnxruntime-gpu>=1.16.1"`
   - `pip install opencv-python`
   - `pip install tqdm`
8. Type `deactivate`, you can close your Terminal or Console and start your SD WebUI, ReActor should start OK - if not, welcome to the Issues section.

### **III. "TypeError: UpscaleOptions.init() got an unexpected keyword argument 'do_restore_first'"**

First of all - you need to disable any other Roop-based extensions:
- Go to 'Extensions -> Installed' tab and uncheck any Roop-based extensions except this one
  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/roop-off.png?raw=true" alt="uncompatible-with-other-roop"/>
- Click 'Apply and restart UI'

Alternative solutions: 
- https://github.com/Gourieff/sd-webui-reactor/issues/3#issuecomment-1615919243
- https://github.com/Gourieff/sd-webui-reactor/issues/39#issuecomment-1666559134 (can be actual, if you use Vladmandic SD.Next)

### **IV. "AttributeError: 'FaceSwapScript' object has no attribute 'enable'"**

Probably, you need to disable the "SD-CN-Animation" extension (or perhaps some another that causes the conflict)

### **V. "INVALID_PROTOBUF : Load model from <...>\models\insightface\inswapper_128.onnx failed:Protobuf parsing failed" OR "AttributeError: 'NoneType' object has no attribute 'get'" OR "AttributeError: 'FaceSwapScript' object has no attribute 'save_original'"**

This error may occur if there's smth wrong with the model file `inswapper_128.onnx`

Try to download it manually from [here](https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx)
and put it to the `stable-diffusion-webui\models\insightface` replacing existing one

### **VI. "ValueError: This ORT build has ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'] enabled" OR "ValueError: This ORT build has ['AzureExecutionProvider', 'CPUExecutionProvider'] enabled"**

1. Close (stop) your SD WebUI Server if it's running
2. Go to the (Windows)`venv\Lib\site-packages` or (MacOS/Linux)`venv/lib/python3.10/site-packages` and see if there are any folders with names start from "~" (for example "~rotobuf"), delete them
3. Go to the (Windows)`venv\Scripts` or (MacOS/Linux)`venv/bin` run Terminal or Console (cmd) there and type `activate`
4. Then:
- `python -m pip install -U pip`
- `pip uninstall -y onnxruntime onnxruntime-gpu onnxruntime-silicon onnxruntime-extensions`
- `pip install "onnxruntime-gpu>=1.16.1"`

If it didn't help - it seems that you have another extension reinstalling `onnxruntime` when SD WebUI checks requirements. Please see your extensions list. Some extensions can causes reinstalling of `onnxruntime-gpu` to `onnxruntime<1.16.1` every time SD WebUI runs.<br>ORT 1.16.0 has a bug https://github.com/microsoft/onnxruntime/issues/17631 - don't install it!

### **VII. "ImportError: cannot import name 'builder' from 'google.protobuf.internal'"**

1. Close (stop) your SD WebUI Server if it's running
2. Go to the (Windows)`venv\Lib\site-packages` or (MacOS/Linux)`venv/lib/python3.10/site-packages` and see if there are any folders with names start from "~" (for example "~rotobuf"), delete them
3. Go to the "google" folder (inside the "site-packages") and delete any folders there with names start from "~"
4. Go to the (Windows)`venv\Scripts` or (MacOS/Linux)`venv/bin` run Terminal or Console (cmd) there and type `activate`
5. Then:
- `python -m pip install -U pip`
- `pip uninstall protobuf`
- `pip install "protobuf>=3.20.3"`

If this method doesn't help - there is some other extension that has a wrong version of protobuf dependence and SD WebUI installs it on a startup requirements check

<a name="insightfacebuild">

### **VIII. (For Windows users) If you still cannot build Insightface for some reasons or just don't want to install Visual Studio or VS C++ Build Tools - do the following:**

1. Close (stop) your SD WebUI Server if it's running
2. Download and put [prebuilt Insightface package](https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp310-cp310-win_amd64.whl) into the stable-diffusion-webui (or SD.Next) root folder where you have "webui-user.bat" file or (A1111 Portable) "run.bat"
3. From stable-diffusion-webui (or SD.Next) root folder run CMD and `.\venv\Scripts\activate`<br>OR<br>(A1111 Portable) Run CMD
4. Then update your PIP: `python -m pip install -U pip`<br>OR<br>(A1111 Portable)`system\python\python.exe -m pip install -U pip`
5. Then install Insightface: `pip install insightface-0.7.3-cp310-cp310-win_amd64.whl`<br>OR<br>(A1111 Portable)`system\python\python.exe -m pip install insightface-0.7.3-cp310-cp310-win_amd64.whl`
6. Enjoy!

### **IX. 07-August-23 Update problem**

If after `git pull` you see the message: `Merge made by the 'recursive' strategy` and then when you check `git status` you see `Your branch is ahead of 'origin/main' by`

Please do the next:

Inside the folder `extensions\sd-webui-reactor-sfw` run Terminal or Console (cmd) and then:
- `git reset f48bdf1 --hard`
- `git pull`

OR

Just delete the folder `sd-webui-reactor-sfw` inside the `extensions` directory and then run Terminal or Console (cmd) and type `git clone https://github.com/Gourieff/sd-webui-reactor-sfw`

### **X. StabilityMatrix Issues**

If you encounter any issues with installing this extension in the StabilityMatrix package manager - read here how to solve: https://github.com/Gourieff/sd-webui-reactor/issues/129#issuecomment-1768210875

## Updating

A good and quick way to check for Extensions updates: https://github.com/Gourieff/sd-webui-extensions-updater

## ComfyUI

You can use ReActor with ComfyUI.<br>
For the installation instruction follow the [ReActor Node repo](https://github.com/Gourieff/ComfyUI-ReActor)

## Disclaimer

This software is meant to be a productive contribution to the rapidly growing AI-generated media industry. It will help artists with tasks such as animating a custom character or using the character as a model for clothing etc.

The developers of this software are aware of its possible unethical application and are committed to take preventative measures against them. We will continue to develop this project in the positive direction while adhering to law and ethics.

Users of this software are expected to use this software responsibly while abiding the local law. If face of a real person is being used, users are suggested to get consent from the concerned person and clearly mention that it is a deepfake when posting content online. **Developers and Contributors of this software are not responsible for actions of end-users.**

By using this extension you are agree not to create any content that:
- violates any laws;
- causes any harm to a person or persons;
- propogates (spreads) any information (both public or personal) or images (both public or personal) which could be meant for harm;
- spreads misinformation;
- targets vulnerable groups of people.

This software utilizes the pre-trained models `buffalo_l` and `inswapper_128.onnx`, which are provided by [InsightFace](https://github.com/deepinsight/insightface/). These models are included under the following conditions:

[From insighface licence](https://github.com/deepinsight/insightface/tree/master/python-package): The InsightFace’s pre-trained models are available for non-commercial research purposes only. This includes both auto-downloading models and manually downloaded models.

Users of this software must strictly adhere to these conditions of use. The developers and maintainers of this software are not responsible for any misuse of InsightFace’s pre-trained models.

Please note that if you intend to use this software for any commercial purposes, you will need to train your own models or find models that can be used commercially.

### Models Hashsum

#### Safe-to-use models have the folowing hash:

inswapper_128.onnx
```
MD5:a3a155b90354160350efd66fed6b3d80
SHA256:e4a3f08c753cb72d04e10aa0f7dbe3deebbf39567d4ead6dce08e98aa49e16af
```

1k3d68.onnx

```
MD5:6fb94fcdb0055e3638bf9158e6a108f4
SHA256:df5c06b8a0c12e422b2ed8947b8869faa4105387f199c477af038aa01f9a45cc
```

2d106det.onnx

```
MD5:a3613ef9eb3662b4ef88eb90db1fcf26
SHA256:f001b856447c413801ef5c42091ed0cd516fcd21f2d6b79635b1e733a7109dbf
```

det_10g.onnx

```
MD5:4c10eef5c9e168357a16fdd580fa8371
SHA256:5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91
```

genderage.onnx

```
MD5:81c77ba87ab38163b0dec6b26f8e2af2
SHA256:4fde69b1c810857b88c64a335084f1c3fe8f01246c9a191b48c7bb756d6652fb
```

w600k_r50.onnx

```
MD5:80248d427976241cbd1343889ed132b3
SHA256:4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43
```

**Please check hashsums if you download these models from unverified (or untrusted) sources**
