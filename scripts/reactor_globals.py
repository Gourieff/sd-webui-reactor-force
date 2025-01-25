import os
from pathlib import Path

try:
    from modules.paths_internal import models_path
except:
    try:
        from modules.paths import models_path
    except:
        models_path = os.path.abspath("models")

IS_RUN: bool = False
BASE_PATH = os.path.join(Path(__file__).parents[1])
DEVICE_LIST: list = ["CPU", "CUDA"]

MODELS_PATH = models_path
SWAPPER_MODELS_PATH = os.path.join(MODELS_PATH, "insightface")
REACTOR_MODELS_PATH = os.path.join(MODELS_PATH, "reactor")
FACE_MODELS_PATH = os.path.join(REACTOR_MODELS_PATH, "faces")

IS_SDNEXT = False

if not os.path.exists(REACTOR_MODELS_PATH):
    os.makedirs(REACTOR_MODELS_PATH)
    if not os.path.exists(FACE_MODELS_PATH):
        os.makedirs(FACE_MODELS_PATH)

def updateDevice():
    try:
        LAST_DEVICE_PATH = os.path.join(BASE_PATH, "last_device.txt")
        with open(LAST_DEVICE_PATH) as f:
            device = f.readline().strip()
        if device not in DEVICE_LIST:
            print(f"Error: Device {device} is not in DEVICE_LIST")
            device = DEVICE_LIST[0]
            print(f"Execution Provider has been set to {device}")
    except Exception as e:
        device = DEVICE_LIST[0]
        print(f"Error: {e}\nExecution Provider has been set to {device}")
    return device

DEVICE = updateDevice()
