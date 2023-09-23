import subprocess
import os, sys
import pkg_resources
from tqdm import tqdm
import urllib.request
from packaging import version as pv

from modules.paths_internal import models_path

req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")

models_dir_old = os.path.join(models_path, "roop")
models_dir = os.path.join(models_path, "insightface")
if os.path.exists(models_dir_old):
    os.rename(models_dir_old, models_dir)
model_url = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"
model_name = os.path.basename(model_url)
model_path = os.path.join(models_dir, model_name)

def run_pip(*args):
    subprocess.run([sys.executable, "-m", "pip", "install", *args])

def is_installed (
        package: str, version: str | None = None, strict: bool = True
):
    has_package = None
    try:
        has_package = pkg_resources.get_distribution(package)
        if has_package is not None:
            installed_version = has_package.version
            if (installed_version != version and strict == True) or (pv.parse(installed_version) < pv.parse(version) and strict == False):
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def download(url, path):
    request = urllib.request.urlopen(url)
    total = int(request.headers.get('Content-Length', 0))
    with tqdm(total=total, desc='Downloading...', unit='B', unit_scale=True, unit_divisor=1024) as progress:
        urllib.request.urlretrieve(url, path, reporthook=lambda count, block_size, total_size: progress.update(block_size))

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(model_path):
    download(model_url, model_path)

print("Checking ReActor requirements...", end=' ')
with open(req_file) as file:
    install_count = 0
    strict = True
    for package in file:
        package_version = None
        try:
            package = package.strip()
            if "==" in package:
                package_version = package.split('==')[1]
            elif ">=" in package:
                package_version = package.split('>=')[1]
                strict = False
            if not is_installed(package,package_version,strict):
                install_count += 1
                run_pip(package)
        except Exception as e:
            print(e)
            print(f"\nERROR: Failed to install {package} - ReActor won't start")
            raise e
    if install_count > 0:
        print(f'\n--- PLEASE, RESTART the Server! ---\n')
    else:
        print('Ok')
