<div align="center">

  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/ReActor_logo_NEW_RU.png?raw=true" alt="logo" width="180px"/>
    
  ![Version](https://img.shields.io/badge/версия-0.7.1_beta3-green?style=for-the-badge&labelColor=darkgreen)
  
  <a href="https://boosty.to/artgourieff" target="_blank">
    <img src="https://lovemet.ru/img/boosty.jpg" width="108" alt="Поддержать проект на Boosty"/>
    <br>
    <sup>
      Поддержать проект
    </sup>
  </a>
  
  <hr>
  
  [![Commit activity](https://img.shields.io/github/commit-activity/t/Gourieff/sd-webui-reactor-sfw/main?cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-sfw/commits/main)
  ![Last commit](https://img.shields.io/github/last-commit/Gourieff/sd-webui-reactor-sfw/main?cacheSeconds=0)
  [![Opened issues](https://img.shields.io/github/issues/Gourieff/sd-webui-reactor-sfw?color=red)](https://github.com/Gourieff/sd-webui-reactor-sfw/issues?cacheSeconds=0)
  [![Closed issues](https://img.shields.io/github/issues-closed/Gourieff/sd-webui-reactor-sfw?color=green&cacheSeconds=0)](https://github.com/Gourieff/sd-webui-reactor-sfw/issues?q=is%3Aissue+is%3Aclosed)
  ![License](https://img.shields.io/github/license/Gourieff/sd-webui-reactor-sfw)

  [English](/README.md) | Русский

# ReActor для Stable Diffusion
### Расширение для быстрой и простой замены лиц на любых изображениях. С фильтром цензуры (встроенный NSFW-детектор исключает замену лиц на изображениях с контентом 18+).

> Используя данное ПО, вы понимаете и принимаете [ответственность](#disclaimer)

---
  <b>
    <a href="#latestupdate">Что нового</a> | <a href="#installation">Установка</a> | <a href="#features">Возможности</a> | <a href="#usage">Использование</a> | <a href="#api">API</a> | <a href="#troubleshooting">Устранение проблем</a> | <a href="#updating">Обновление</a> | <a href="#comfyui">ComfyUI</a> | <a href="#disclaimer">Ответственность</a>
  </b>
</div>

---

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/demo_crop.jpg?raw=true" alt="example"/>

<a name="latestupdate">

## Что нового в последних обновлениях

### 0.7.1 <sub><sup>BETA1

- Использование пробелов в индексах лиц (пример: 0, 1, 2)
- Список моделей лиц теперь отсортирован по алфавиту
- [API для создания моделей лиц](./API.md#facemodel-build-api)
- Правки и улучшения

<details>
	<summary><a>Нажмите, чтобы посмотреть больше</a></summary>

### 0.7.0 <sub><sup>BETA2

- X/Y/Z опция улучшена! Добавлен ещё один параметр: теперь вы можете выбрать несколько моделей лиц для создания вариации замененных лиц, чтобы выбрать наилучшие!

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-05.jpg?raw=true" alt="0.7.0-whatsnew-05" width="100%"/>

Чтобы использовать ось "Face Model" - активируйте РеАктор и выбирите любую модель лица в качестве источника:<br>
<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-07.jpg?raw=true" alt="0.7.0-whatsnew-07" width="50%"/><img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-06.jpg?raw=true" alt="0.7.0-whatsnew-06" width="50%"/>

Полноразмерное демо-изображение: [xyz_demo_2.png](https://raw.githubusercontent.com/Gourieff/Assets/main/sd-webui-reactor/xyz_demo_2.png)

### 0.7.0 <sub><sup>BETA1

- Поддержка X/Y/Z скрипта (до 3-х параметров: CodeFormer Weight, Restorer Visibility, Face Mask Correction)

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-03.jpg?raw=true" alt="0.7.0-whatsnew-03" width="100%"/>

Полноразмерное демо-изображение: [xyz_demo.png](https://raw.githubusercontent.com/Gourieff/Assets/main/sd-webui-reactor/xyz_demo.png)

### 0.7.0 <sub><sup>ALPHA1

- По многочисленным просьбам появилась возможность строить смешанные модели лиц ("Tools->Face Models->Blend")

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-01.jpg?raw=true" alt="0.7.0-whatsnew-01" width="100%"/><img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/0.7.0-whatsnew-02.jpg?raw=true" alt="0.7.0-whatsnew-02" width="100%"/>

- Поддержка CUDA 12 в скрипте установщика для библиотеки ORT-GPU версии 1.17.0
- Новая вкладка "Detection" с параметрами "Threshold" и "Max Faces"

### 0.6.1 <sub><sup>BETA3

- Опция 'Force Upscale' внутри вкладки 'Upscale': апскейл выполнится, даже если не было обнаружено ни одного лица (FR https://github.com/Gourieff/sd-webui-reactor/issues/116)
- Отображение имён файлов используемых изображений, когда выбрано несколько изображений или папка (а также режим случайного изображения)

### 0.6.1 <sub><sup>BETA2

- Опция 'Save original' теперь работает правильно, когда вы выбираете 'Multiple Images' или 'Source Folder'
- Добавлен режим выбора случайного изображения для 'Source Folder'

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/random_from_folder_demo_01.jpg?raw=true" alt="0.6.1-whatsnew-01" width="100%"/>

### 0.6.0

- Новый логотип
- Адаптация к версии A1111 1.7.0 (правильная загрузка GFPGAN)
- Новая ссылка для файла основной модели
- UI переработан
- Появилась возможность загружать несколько исходных изображений с лицами или задавать путь к папке, содержащей такие изображения

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/multiple_source_images_demo_01.png?raw=true" alt="0.6.0-whatsnew-01" width="100%"/>

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/multiple_source_images_demo_02.png?raw=true" alt="0.6.0-whatsnew-02" width="100%"/>

### 0.5.1

- Теперь можно сохранять модели лиц в качестве файлов "safetensors" (находятся в `<sd-web-ui-folder>\models\reactor\faces`) и загружать их с ReActor, храня супер легкие модели лиц, которые вы чаще всего используете;
- Новые опция "Face Mask Correction" - если вы сталкиваетесь с пикселизацией вокруг контуров лица, эта опция будет полезной;

<img src="https://github.com/Gourieff/Assets/blob/main/sd-webui-reactor/face_model_demo_01.jpg?raw=true" alt="0.5.0-whatsnew-01" width="100%"/>

</details>

<a name="installation">

## Установка

[A1111 WebUI / WebUI-Forge](#a1111) | [SD.Next](#sdnext) | [Google Colab SD WebUI](#colab)

<a name="a1111">Если вы используете [AUTOMATIC1111 SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui/) или [SD WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge):

1. (Для пользователей Windows):
  - Установите **Visual Studio 2022** (Например, версию Community - этот шаг нужен для правильной компиляции библиотеки Insightface):
  https://visualstudio.microsoft.com/downloads/
  - ИЛИ только **VS C++ Build Tools** (если вам не нужен весь пакет Visual Studio), выберите "Desktop Development with C++" в разделе "Workloads -> Desktop & Mobile":
  https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - ИЛИ если же вы не хотите устанавливать что-либо из вышеуказанного - выполните [следующие шаги (пункт VIII)](#insightfacebuild)
2. Внутри SD Web-UI перейдите во вкладку "Extensions", загрузите список доступных расширений (вкладка "Available") и введите "ReActor" в строке поиска или же вставьте ссылку `https://github.com/Gourieff/sd-webui-reactor-sfw` в "Install from URL" - и нажмите "Install"
3. Пожалуйста, подождите несколько минут, пока процесс установки полностью не завершится (наберитесь терпения, не прерывайте процесс)
4. Проверьте последнее сообщение в консоли SD-WebUI:
* Если вы видите "--- PLEASE, RESTART the Server! ---" - остановите Сервер (CTRL+C или CMD+C) и запустите его заново - ИЛИ же перейдите во вкладку "Installed", нажмите "Apply and restart UI" 
* Если вы видите "Done!", просто перезагрузите UI, нажав на "Reload UI"
5. Готово!

<a name="sdnext">Если вы используете [SD.Next](https://github.com/vladmandic/automatic):

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. (Для пользователей Windows) Смотрите [Шаг 1](#a1111) для Automatic1111 (если же вы следовали [данным шагам (пункт VIII)](#insightfacebuild) вместо этого - переходите к Шагу 5)
3. Перейдите в (Windows)`automatic\venv\Scripts` или (MacOS/Linux)`automatic/venv/bin`, запустите Терминал или Консоль (cmd) для данной папки и выполните `activate`
4. Выполните `pip install insightface==0.7.3`
5. Запустите SD.Next, перейдите во вкладку "Extensions", вставьте эту ссылку `https://github.com/Gourieff/sd-webui-reactor-sfw` в "Install from URL" и нажмите "Install"
6. Пожалуйста, подождите несколько минут, пока процесс установки полностью не завершится (наберитесь терпения, не прерывайте процесс)
7. Проверьте последнее сообщение в консоли SD.Next:
* Если вы видите "--- PLEASE, RESTART the Server! ---" - остановите Сервер (CTRL+C или CMD+C) или просто закройте консоль
8. Перейдите в директорию `automatic\extensions\sd-webui-reactor-sfw` - если вы видите там папку `models\insightface` с файлом `inswapper_128.onnx` внутри, переместите его в папку `automatic\models\insightface`
9. Готово, можете запустить SD.Next WebUI!

<a name="colab">Если вы используете [Cagliostro Colab UI](https://github.com/Linaqruf/sd-notebook-collection):

1. В активном WebUI перейдите во вкладку "Extensions", загрузите список доступных расширений (вкладка "Available") и введите "ReActor" в строке поиска или же вставьте ссылку `https://github.com/Gourieff/sd-webui-reactor-sfw` в "Install from URL" - и нажмите "Install"
2. Пожалуйста, подождите некоторое время, пока процесс установки полностью не завершится (наберитесь терпения, не прерывайте процесс)
3. Когда вы увидите сообщение "--- PLEASE, RESTART the Server! ---" (в секции "Start UI" вашего ноутбука "Start Cagliostro Colab UI") - перейдите во вкладку "Installed" и нажмите "Apply and restart UI"
4. Готово!

<a name="features">

## Возможности

- Быстрая и точна **замена лиц (faceswap)** на изображении
- **Поддержка нескольких лиц**
- **Определение пола**
- Функция **сохранения оригинального изображения** (сгенерированного до замены лица)
- **Восстановление лица** после замены
- **Увеличение размера** полученного изображения
- Сохранение и загрузка **Моделей Лиц типа Safetensors**
- **Коррекция Маски Лица** для предотвращения какой-либо пикселизации вокруг контуров лиц
- Возможность задать **порядок постобработки**
- **100% совместимость** с разными **SD WebUI**: Automatic1111, SD.Next, Cagliostro Colab UI
- **Отличная производительность** даже с использованием ЦПУ, ReActor для SD WebUI абсолютно не требователен к мощности вашей видеокарты
- **Поддержка CUDA**, начиная с версии 0.5.0
- **Поддержка [API](/API.md)**: как встроенного в SD WebUI, так и внешнего (через POST/GET запросы)
- **[Поддержка](https://github.com/Gourieff/ComfyUI-ReActor) ComfyUI**
- **[Поддержка](https://github.com/Gourieff/sd-webui-reactor/issues/42) компьютеров Mac M1/M2**
- **Регулировка уровня логов** консоли
- **Без NSFW фильтров** (данное расширение адресовано высокоразвитым интеллектуальным людям, а не извращенцам; наше общество должно быть ориентировано на своём пути на высшие стандарты, а не на низшие - в этом состоит суть развития и эволюции человеческого общества; поэтому, моя позиция такова - что зрелые умом люди достаточно разумны, чтобы понимать, что есть хорошо, а что плохо и нести полную ответственность за собственные действия; для прочих - никакие "фильтры" не помогут, пока эти люди сами не поймут, как работает Вселенная)

<a name="usage">

## Использование

> Используя данное программное обеспечение, вы соглашаетесь с [ответственностью](#disclaimer)

1. В раскрывающимся меню "ReActor" импортируйте изображение, содержащее лицо;
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

### Img2Img

Используйте эту вкладку, чтобы заменить лицо на уже готовом изображении (флажок "Swap in source image") или на сгенерированном на основе готового (флажок "Swap in generated image").

Inpainting также работает, но замена лица происходит только в области маски.<br>Пожалуйста, используйте с опцией "Only masked" для "Inpaint area", если вы применяете "Upscaler". Иначе, используйте функцию увеличения (апскейла) через вкладку "Extras" или через опциональный загрузчик "Script" (внизу экрана), применив "SD upscale" или "Ultimate SD upscale".

### Extras

Начиная с версии 0.5.0, вы можете использовать ReActor через вкладку Extras, что даёт очень быструю производительность и возможность замены лиц в обход пайплайна SD, что иногда вызывает размытие или искажение деталей оригинального изображения

<img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/extras_tab.jpg?raw=true" alt="IamSFW"/>

## API

Вы можете использовать ReActor как со встроенным SD Webui API так и через внешнее API.

Подробная инструкция **[здесь](/API.md)**.

<a name="troubleshooting">

## Устранение проблем

### **I. "You should at least have one model in models directory"**

Проверьте путь, где хранится модель "inswapper_128.onnx". Файл должен находиться в папке `stable-diffusion-webui\models\insightface`. Переместите модель туда, если она находится в какой-то иной директории.

### **II. Какие-либо проблемы с установкой Insightface или прочих пакетов**

(Для пользователей Mac M1/M2) Если вы получаете ошибки в ходе установки Insightface - читайте https://github.com/Gourieff/sd-webui-reactor/issues/42

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
   - `pip install "onnxruntime-gpu>=1.16.1"`
   - `pip install opencv-python`
   - `pip install tqdm`
8. Выполните `deactivate`, закройте Терминал или Консоль и запустите SD WebUI, ReActor должен запуститься без к-л проблем - если же нет, добро пожаловать в раздел "Issues".

### **III. "TypeError: UpscaleOptions.init() got an unexpected keyword argument 'do_restore_first'"**

Для начала отключите любые другие Roop-подобные расширения:
- Перейдите в 'Extensions -> Installed' и снимите флажок с ненужных:
  <img src="https://github.com/Gourieff/Assets/raw/main/sd-webui-reactor/roop-off.png?raw=true" alt="uncompatible-with-other-roop"/>
- Нажмите 'Apply and restart UI'

Альтернативные решения: 
- https://github.com/Gourieff/sd-webui-reactor/issues/3#issuecomment-1615919243
- https://github.com/Gourieff/sd-webui-reactor/issues/39#issuecomment-1666559134 (актуально для Vladmandic SD.Next)

### **IV. "AttributeError: 'FaceSwapScript' object has no attribute 'enable'"**

Отключите расширение "SD-CN-Animation" (или какое-либо другое, вызывающее конфликт)

### **V. "INVALID_PROTOBUF : Load model from <...>\models\insightface\inswapper_128.onnx failed:Protobuf parsing failed" ИЛИ "AttributeError: 'NoneType' object has no attribute 'get'" ИЛИ "AttributeError: 'FaceSwapScript' object has no attribute 'save_original'"**

Эта ошибка появляется, если что-то не так с файлом модели `inswapper_128.onnx`.

Скачайте вручную по ссылке [here](https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx)
и сохраните в директорию `stable-diffusion-webui\models\insightface`, заменив имеющийся файл.

### **VI. "ValueError: This ORT build has ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'] enabled" ИЛИ "ValueError: This ORT build has ['AzureExecutionProvider', 'CPUExecutionProvider'] enabled"**

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Перейдите в (Windows)`venv\Lib\site-packages` или (MacOS/Linux)`venv/lib/python3.10/site-packages` и посмотрите, если там папки с именам, начинающимися на "~" (например, "~rotobuf"), удалите их
3. Перейдите в (Windows)`venv\Scripts` или (MacOS/Linux)`venv/bin`, откройте Терминал или Консоль (cmd) и выполните `activate`
4. Затем:
- `python -m pip install -U pip`
- `pip uninstall -y onnxruntime onnxruntime-gpu onnxruntime-silicon onnxruntime-extensions`
- `pip install "onnxruntime-gpu>=1.16.1"`

Если это не помогло - значит какое-то другое расширение переустанавливает `onnxruntime` всякий раз, когда SD WebUI проверяет требования пакетов. Внимательно посмотрите список активных расширений. Некоторые расширения могут вызывать переустановку `onnxruntime-gpu` на версию `onnxruntime<1.16.1` при каждом запуске SD WebUI.<br>ORT 1.16.0 выкатили с ошибкой https://github.com/microsoft/onnxruntime/issues/17631 - не устанавливайте её!

### **VII. "ImportError: cannot import name 'builder' from 'google.protobuf.internal'"**

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Перейдите в (Windows)`venv\Lib\site-packages` или (MacOS/Linux)`venv/lib/python3.10/site-packages` и посмотрите, если там папки с именам, начинающимися на "~" (например, "~rotobuf"), удалите их
3. Перейдите в папку "google" (внутри "site-packages") и удалите любые папки с именам, начинающимися на "~"
4. Перейдите в (Windows)`venv\Scripts` или (MacOS/Linux)`venv/bin`, откройте Терминал или Консоль (cmd) и выполните `activate`
5. Затем:
- `python -m pip install -U pip`
- `pip uninstall protobuf`
- `pip install "protobuf>=3.20.3"`

Если это не помгло - значит, есть к-л другое расширение, которое использует неподходящую версию пакета protobuf, и SD WebUI устанавливает эту версию при каждом запуске.

<a name="insightfacebuild">

### **VIII. (Для пользователей Windows) Если вы до сих пор не можете установить пакет Insightface по каким-то причинам или же просто не желаете устанавливать Visual Studio или VS C++ Build Tools - сделайте следующее:**

1. Закройте (остановите) SD WebUI Сервер, если он запущен
2. Скачайте готовый [пакет Insightface](https://github.com/Gourieff/Assets/raw/main/Insightface/insightface-0.7.3-cp310-cp310-win_amd64.whl) и сохраните его в корневую директорию stable-diffusion-webui (или SD.Next) - туда, где лежит файл "webui-user.bat" или (A1111 Portable) "run.bat"
3. Из корневой директории откройте Консоль (CMD) и выполните `.\venv\Scripts\activate`<br>ИЛИ<br>(A1111 Portable) Откройте Консоль (CMD)
4. Обновите PIP: `python -m pip install -U pip`<br>ИЛИ<br>(A1111 Portable)`system\python\python.exe -m pip install -U pip`
5. Затем установите Insightface: `pip install insightface-0.7.3-cp310-cp310-win_amd64.whl`<br>ИЛИ<br>(A1111 Portable)`system\python\python.exe -m pip install insightface-0.7.3-cp310-cp310-win_amd64.whl`
6. Готово!

### **IX. Ошибка обновления 07-Август-23**

Если после очередного `git pull` вы получили сообщение: `Merge made by the 'recursive' strategy` и затем, когда проверяете статус репозитория через `git status`, вы видите `Your branch is ahead of 'origin/main' by`

Выполните следующее:

Внутри папки `extensions\sd-webui-reactor-sfw` запустите Терминал или Консоль (cmd) и затем:
- `git reset f48bdf1 --hard`
- `git pull`

ИЛИ:

Полностью удалите папку `sd-webui-reactor-sfw` внутри директории `extensions`, запустите Терминал или Консоль (cmd) и выполните `git clone https://github.com/Gourieff/sd-webui-reactor-sfw`

### **X. Ошибки установки в StabilityMatrix**

Если вы столкнулись с ошибками при установки данного расширения в пакетном менеджере StabilityMatrix - изучите информацию по ссылке: https://github.com/Gourieff/sd-webui-reactor/issues/129#issuecomment-1768210875

<a name="updating">

## Обновление

Самый простой и удобный способ обновления SD WebUI и расширений: https://github.com/Gourieff/sd-webui-extensions-updater

## ComfyUI

Вы можете использовать ReActor с ComfyUI<br>
Инструкция здесь: [ReActor Node](https://github.com/Gourieff/ComfyUI-ReActor)

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
