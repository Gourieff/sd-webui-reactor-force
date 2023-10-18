<div align="center">

  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/ReActor_logo_red_CUDA.png?raw=true" alt="logo" width="180px"/>
    
  ![Version](https://img.shields.io/badge/версия-0.4.3_beta2-green?style=for-the-badge&labelColor=darkgreen)
  
  <table>
    <tr>
      <td width="50%">
        <a href="https://github.com/Gourieff/sd-webui-reactor" target="_blank">
          для любых GPU
          <br>
          <sup>
            NVIDIA / AMD / Intel
          </sup>
        </a>
      </td>
      <td width="158px">
        <b>
          для GPU NVIDIA
        </b>
        <br>
        <sup>
          8Гб VRAM или более
        </sup>
      </td>
    </tr>
  </table>
  
  <hr>
  
  [![Commit activity](https://img.shields.io/github/commit-activity/t/Gourieff/sd-webui-reactor-force/main?cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-force/commits/main)
  ![Last commit](https://img.shields.io/github/last-commit/Gourieff/sd-webui-reactor-force/main?cacheSeconds=0)
  [![Opened issues](https://img.shields.io/github/issues/Gourieff/sd-webui-reactor-force?color=red)](https://github.com/Gourieff/sd-webui-reactor-force/issues?cacheSeconds=0)
  [![Closed issues](https://img.shields.io/github/issues-closed/Gourieff/sd-webui-reactor-force?color=green&cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-force/issues?q=is%3Aissue+is%3Aclosed)
  ![License](https://img.shields.io/github/license/Gourieff/sd-webui-reactor-force)

  [English](/README.md) | Русский

# ReActor Force для Stable Diffusion

### Расширение для быстрой и простой замены лиц на любых изображениях. Без фильтра цензуры, 18+, используйте под вашу собственную [ответственность](#disclaimer)

</div>

---
<div align="center">
  <b>
    <a href="#installation">Установка</a> | <a href="#features">Возможности</a> | <a href="#usage">Использование</a> | <a href="#api">API</a> | <a href="#troubleshooting">Устранение проблем</a> | <a href="#updating">Обновление</a> | <a href="#comfyui">ComfyUI</a> | <a href="#disclaimer">Ответственность</a>
  </b>
</div>

---

<table>
  <tr>
    <td width="134px">
      <a href="https://boosty.to/artgourieff" target="_blank">
        <img src="https://lovemet.ru/www/boosty.jpg" width="108" alt="Поддержать проект на Boosty"/>
        <br>
        <sup>
          Поддержать проект
        </sup>
      </a>
    </td>
    <td>
      ReActor это расширение для Stable Diffusion WebUI, которое позволяет делать простую и точную замену лиц на изображениях. Сделано на основе <a href="https://github.com/Gourieff/sd-webui-reactor" target="_blank">SD WebUI ReActor</a>.
    </td>
    <td width="144px">
      <a href="https://paypal.me/artgourieff" target="_blank">
        <img src="https://www.paypalobjects.com/digitalassets/c/website/logo/full-text/pp_fc_hl.svg" width="108" alt="Поддержать проект через PayPal"/>
        <br>
        <sup>
          Помочь проекту
        </sup>
      </a>
    </td>
  </tr>
</table>

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/demo_crop.jpg?raw=true" alt="example"/>

<a name="installation">

## Установка

[Automatic1111](#a1111) | [Vladmandic SD.Next](#sdnext) | [Google Colab SD WebUI](#colab)

<a name="a1111">Если вы используете [AUTOMATIC1111 Web-UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui/):

1. (Для пользователей Windows):
  - Установите **Visual Studio 2022** (Например, версию Community - этот шаг нужен для правильной компиляции библиотеки Insightface):
  https://visualstudio.microsoft.com/downloads/
  - ИЛИ только **VS C++ Build Tools** (если вам не нужен весь пакет Visual Studio), выберите "Desktop Development with C++" в разделе "Workloads -> Desktop & Mobile":
  https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - ИЛИ если же вы не хотите устанавливать что-либо из вышеуказанного - выполните [следующие шаги (пункт VIII)](#insightfacebuild)
2. Внутри SD Web-UI перейдите во вкладку "Extensions" и вставьте ссылку `https://github.com/Gourieff/sd-webui-reactor-force` в "Install from URL" и нажмите "Install"
3. Пожалуйста, подождите несколько минут, пока процесс установки полностью не завершится
4. Проверьте последнее сообщение в консоли SD-WebUI:
* Если вы видите "--- PLEASE, RESTART the Server! ---" - остановите Сервер (CTRL+C или CMD+C) и запустите его заново - ИЛИ же перейдите во вкладку "Installed" (*если у вас имееются какие-либо другие расширение, основанные на Roop или клонах ReActor - отключите их, иначе данное расширение может не работать*), нажмите "Apply and restart UI" 
* Если вы видите "Done!", перейдите во вкладку "Installed" (*если у вас имееются какие-либо другие расширение, основанные на Roop или клонах ReActor - отключите их, иначе данное расширение может не работать*), нажмите "Apply and restart UI" - или же просто перезагрузите UI, нажав на "Reload UI"
5. Готово!

<a name="sdnext">Если вы используете [SD.Next](https://github.com/vladmandic/automatic):

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. (Для пользователей Windows) Смотрите [Шаг 1](#a1111) для Automatic1111 (если же вы следовали [данным шагам (пункт VIII)](#insightfacebuild) вместо этого - переходите к Шагу 5)
3. Перейдите в (Windows)`automatic\venv\Scripts` или (MacOS/Linux)`automatic/venv/bin`, запустите Терминал или Консоль (cmd) для данной папки и выполните `activate`
4. Выполните `pip install insightface==0.7.3`
5. Запустите SD.Next, перейдите во вкладку "Extensions", вставьте эту ссылку `https://github.com/Gourieff/sd-webui-reactor-force` в "Install from URL" и нажмите "Install"
6. Пожалуйста, подождите несколько минут, пока процесс установки полностью не завершится
7. Проверьте последнее сообщение в консоли SD.Next:
* Если вы видите "--- PLEASE, RESTART the Server! ---" - остановите Сервер (CTRL+C или CMD+C) и запустите его заново - ИЛИ же перейдите во вкладку "Installed" (*если у вас имееются какие-либо другие расширение, основанные на Roop или клонах ReActor - отключите их, иначе данное расширение может не работать*), нажмите "Restart the UI"
8. Остановите Сервер SD.Next, перейдите в директорию `automatic\extensions\sd-webui-reactor-force` - если вы видите там папку `models\insightface` с файлом `inswapper_128.onnx` внутри, переместите его в папку `automatic\models\insightface`
9. Готово, можете запустить SD.Next WebUI!

<a name="colab">Если вы используете [Cagliostro Colab UI](https://github.com/Linaqruf/sd-notebook-collection):

1. В активном WebUI, перейдите во вкладку "Extensions", вставьте ссылку `https://github.com/Gourieff/sd-webui-reactor-force` в "Install from URL" и нажмите "Install"
2. Пожалуйста, подождите некоторое время, пока процесс установки полностью не завершится
3. Когда вы увидите сообщение "--- PLEASE, RESTART the Server! ---" (в секции "Start UI" вашего ноутбука "Start Cagliostro Colab UI") - перейдите во вкладку "Installed" и нажмите "Apply and restart UI" (*если у вас имееются какие-либо другие расширение, основанные на Roop или клонах ReActor - отключите их, иначе данное расширение может не работать*)
4. Готово!

<a name="features">

## Возможности

- Быстрая и точна **замена лиц (faceswap)** на изображении
- **Поддержка нескольких лиц**
- **Определение пола**
- Функция **сохранения оригинального изображения** (сгенерированного до замены лица)
- **Восстановление лица** после замены
- **Увеличение размера** полученного изображения
- Возможность задать **порядок постобработки**
- **100% совместимость** с разными **SD WebUI**: Automatic1111, SD.Next, Cagliostro Colab UI
- **Отличная производительность** с ГП NVIDIA при объёме памяти от 8Гб и более (для остальных случаев используйте [другую версию](https://github.com/Gourieff/sd-webui-reactor) расширения ReActor)
- **Поддержка [API](/API.md)**: как встроенного в SD WebUI, так и внешнего (через POST/GET запросы)
- **[Поддержка](https://github.com/Gourieff/comfyui-reactor-node) ComfyUI**
- **Регулировка уровня логов** консоли
- **Без NSFW фильтров** (данное расширение адресовано высокоразвитым интеллектуальным людям, а не извращенцам; наше общество должно быть ориентировано на своём пути на высшие стандарты, а не на низшие - в этом состоит суть развития и эволюции человеческого общества; поэтому, моя позиция такова - что зрелые умом люди достаточно разумны, чтобы понимать, что есть хорошо, а что плохо и нести полную ответственность за собственные действия; для прочих - никакие "фильтры" не помогут, пока эти люди сами не поймут, как работает Вселенная)

<a name="usage">

## Использование

> Используя данное программное обеспечение, вы соглашаетесь с [ответственностью](#disclaimer)

1. В раскрывающимся меню "ReActor Force" импортируйте изображение, содержащее лицо;
2. Установите флажок "Enable";
3. Готово, теперь результат будет иметь то лицо, которое вы выбрали.

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/example.jpg?raw=true" alt="example" width="808"/>

### Индексы Лиц (Face Indexes)

ReActor определяет лица на изображении в следующей последовательности:<br>
слева-направо, сверху-вниз.

Если вам нужно заменить определенное лицо, вы можете указать индекс для исходного (source, с лицом) и входного (input, где будет замена лица) изображений.

Индекс первого обнаруженного лица - 0.

Вы можете задать индексы в том порядке, который вам нужен.<br>
Например: 0,1,2 (для Source); 1,0,2 (для Input).<br>
Это означает, что: второе лицо из Input (индекс = 1) будет заменено первым лицом из Source (индекс = 0) и так далее.

### Определение Пола

Вы можете обозначить, какой пол нужно определять на изображении.<br>
ReActor заменит только то лицо, которое удовлетворяет заданному условию.

### Если лицо получилось нечётким
Используйте опцию "Restore Face". Также можете попробовать опцию "Upscaler". Для более точного контроля параметров используйте Upscaler во вкладке "Extras".
Также вы можете установить порядок постобработки (начиная с версии 0.1.0):
<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/pp-order.png?raw=true" alt="example"/>

*Прежняя логика была противоположенной (Upscale -> затем Restore), что приводило к более худшему качеству изображения лица (а также к значительной разнице текстур) после увеличения.* 

### Результат имеет несколько лиц
Выберите номера лиц, которые нужно поменять, используя поля "Comma separated face number(s)" для исходного изображения лица и для результата. Можно устанавливать любой, необходимый вам, порядок лиц.
<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/multiple-faces.png?raw=true" alt="example"/>

### ~~Результат получился чёрным~~
~~Это значит, что сработал NSFW фильтр.~~

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/IamSFW.jpg?raw=true" alt="IamSFW" width="50%"/>

### Img2Img

Используйте эту вкладку, чтобы заменить лицо на уже готовом изображении (флажок "Swap in source image") или на сгенерированном на основе готового (флажок "Swap in generated image").

Inpainting также работает, но замена лица происходит только в области маски.<br>Пожалуйста, используйте с опцией "Only masked" для "Inpaint area", если вы применяете "Upscaler". Иначе, используйте функцию увеличения (апскейла) через вкладку "Extras" или через опциональный загрузчик "Script" (внизу экрана), применив "SD upscale" или "Ultimate SD upscale".

## API

Вы можете использовать ReActor как со встроенным SD Webui API так и через внешнее API.

Подробная инструкция **[здесь](/API.md)**.

<a name="troubleshooting">

## Устранение проблем

### **I. "You should at least have one model in models directory"**

Проверьте путь, где хранится модель "inswapper_128.onnx". Файл должен находиться в папке `stable-diffusion-webui\models\insightface`. Переместите модель туда, если она находится в какой-то иной директории.

### **II. Какие-либо проблемы с установкой Insightface или прочих пакетов**

(Для пользователей Mac M1/M2) Если вы получаете ошибки в ходе установки Insightface - читайте https://github.com/Gourieff/sd-webui-reactor/issues/42 и используйте [другую версию](https://github.com/Gourieff/sd-webui-reactor) расширения ReActor

(Для пользователей Windows) Если VS C++ Build Tools или MS VS 2022 установлены но вы видите ошибки, связанные с отсутствием Insightface, попробуйте следующее:
1. Закройте (остановите) SD WebUI Сервер и запустите его снова (возможно, не прошла инициализация пакета после его установки)
   
(Для пользователей любых ОС) Попробуйте следующее:
1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Перейдите в папку (Windows)`venv\Lib\site-packages` или (MacOS/Linux)`venv/lib/python3.10/site-packages`
3. Если вы видите к-л папки с именами, начинающимися с `~` (например, "~rotobuf") - удалите их
4. Перейдите в (Windows)`venv\Scripts` или (MacOS/Linux)`venv/bin`
5. Откройте Терминал или Консоль (cmd) для этой папки и выполните `activate`
6. Для начала обновите pip: `pip install -U pip`
7. Далее:
   - `pip install insightface==0.7.3`
   - `pip install onnx`
   - `pip install onnxruntime-gpu==1.15.1`
   - `pip install opencv-python`
   - `pip install tqdm`
8. Выполните `deactivate`, закройте Терминал или Консоль и запустите SD WebUI, ReActor должен запуститься без к-л проблем - если же нет, добро пожаловать в раздел "Issues".

### **III. "TypeError: UpscaleOptions.init() got an unexpected keyword argument 'do_restore_first'"**

Для начала отключите любые другие Roop-подобные расширения:
- Перейдите в 'Extensions -> Installed' и снимите флажок с ненужных:
  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/roop-off.png?raw=true" alt="uncompatible-with-other-roop"/>
- Нажмите 'Apply and restart UI'

### **IV. "AttributeError: 'FaceSwapScript' object has no attribute 'enable'"**

Отключите расширение "SD-CN-Animation" (или какое-либо другое, вызывающее конфликт)

### **V. "INVALID_PROTOBUF : Load model from <...>\models\insightface\inswapper_128.onnx failed:Protobuf parsing failed" ИЛИ "AttributeError: 'NoneType' object has no attribute 'get'" ИЛИ "AttributeError: 'FaceSwapScript' object has no attribute 'save_original'"**

Эта ошибка появляется, если что-то не так с файлом модели `inswapper_128.onnx`.

Скачайте вручную по ссылке [here](https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx)
и сохраните в директорию `stable-diffusion-webui\models\insightface`, заменив имеющийся файл.

### **VI. "ImportError: cannot import name 'builder' from 'google.protobuf.internal'"**

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Перейдите в (Windows)`venv\Lib\site-packages` или (MacOS/Linux)`venv/lib/python3.10/site-packages` и посмотрите, если там папки с именам, начинающимися на "~" (например, "~rotobuf"), удалите их
3. Перейдите в папку "google" (внутри "site-packages") и удалите любые папки с именам, начинающимися на "~"
4. Перейдите в (Windows)`venv\Scripts` или (MacOS/Linux)`venv/bin`, откройте Терминал или Консоль (cmd) и выполните `activate`
5. Затем:
- `python -m pip install -U pip`
- `pip uninstall protobuf`
- `pip install protobuf>=3.20.3`

Если это не помгло - значит, есть к-л другое расширение, которое использует неподходящую версию пакета protobuf, и SD WebUI устанавливает эту версию при каждом запуске.

<a name="insightfacebuild">

### **VII. (Для пользователей Windows) Если вы до сих пор не можете установить пакет Insightface по каким-то причинам или же просто не желаете устанавливать Visual Studio или VS C++ Build Tools - сделайте следующее:**

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Скачайте готовый [пакет Insightface](https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp310-cp310-win_amd64.whl) и сохраните его в корневую директорию stable-diffusion-webui (или SD.Next) - туда, где лежит файл "webui-user.bat"
3. Из корневой директории откройте Консоль (CMD) и выполните `.\venv\Scripts\activate`
4. Обновите PIP: `python -m pip install -U pip`
5. Затем установите Insightface: `pip install insightface-0.7.3-cp310-cp310-win_amd64.whl`
6. Готово!

<a name="updating">

## Обновление

Самый простой и удобный способ обновления SD WebUI и расширений: https://github.com/Gourieff/sd-webui-extensions-updater

## ComfyUI

Вы можете использовать ReActor с ComfyUI<br>
Инструкция здесь: [ReActor Node](https://github.com/Gourieff/comfyui-reactor-node)

<a name="disclaimer">

## Ответственность

Это программное обеспечение призвано стать продуктивным вкладом в быстрорастущую медиаиндустрию на основе генеративных сетей и искусственного интеллекта. Данное ПО поможет художникам в решении таких задач, как анимация собственного персонажа или использование персонажа в качестве модели для одежды и т.д.

Разработчики этого программного обеспечения осведомлены о возможных неэтичных применениях и обязуются принять против этого превентивные меры. Мы продолжим развивать этот проект в позитивном направлении, придерживаясь закона и этики.

Подразумевается, что пользователи этого программного обеспечения будут использовать его ответственно, соблюдая локальное законодательство. Если используется лицо реального человека, пользователь обязан получить согласие заинтересованного лица и четко указать, что это дипфейк при размещении контента в Интернете. **Разработчики и Со-авторы данного программного обеспечения не несут ответственности за действия конечных пользователей.**

Используя данное расширение, вы соглашаетесь не создавать материалы, которые:
- нарушают какие-либо действующие законы тех или иных государств или международных организаций;
- причиняют какой-либо вред человеку или лицам;
- пропагандируют любую информацию (как общедоступную, так и личную) или изображения (как общедоступные, так и личные), которые могут быть направлены на причинение вреда;
- используются для распространения дезинформации;
- нацелены на уязвимые группы людей.

Данное программное обеспечение использует предварительно обученные модели `buffalo_l` и `inswapper_128.onnx`, представленные разработчиками [InsightFace](https://github.com/deepinsight/insightface/). Эти модели распространяются при следующих условиях:

[Перевод из текста лицензии insighface](https://github.com/deepinsight/insightface/tree/master/python-package): Предварительно обученные модели InsightFace доступны только для некоммерческих исследовательских целей. Сюда входят как модели с автоматической загрузкой, так и модели, загруженные вручную.

Пользователи данного программного обеспечения должны строго соблюдать данные условия использования. Разработчики и Со-авторы данного программного продукта не несут ответственности за неправильное использование предварительно обученных моделей InsightFace.

Обратите внимание: если вы собираетесь использовать это программное обеспечение в каких-либо коммерческих целях, вам необходимо будет обучить свои собственные модели или найти модели, которые можно использовать в коммерческих целях.

### Хэш файлов моделей

#### Безопасные для использования модели имеют следующий хэш:

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

**Пожалуйста, сравните хэш, если вы скачиваете данные модели из непроверенных источников**
