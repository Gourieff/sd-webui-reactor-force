from transformers import pipeline
from PIL import Image
import logging
import torch

SCORE = 0.965 # 0.965 and less - is safety content

logging.getLogger('transformers').setLevel(logging.ERROR)

def nsfw_image(img_path: str, model_path: str):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    with Image.open(img_path) as img:
        predict = pipeline("image-classification", model=model_path)
        predict.model.to(device)
        result = predict(img)
        score = result[0]["score"]
        print(f"NSFW Score = {score}")
        return True if score > SCORE else False
