import cv2
import numpy as np
from PIL import Image, ImageDraw

from torchvision.transforms.functional import to_pil_image

from scripts.reactor_logger import logger
from scripts.reactor_inferencers.bisenet_mask_generator import BiSeNetMaskGenerator
from scripts.reactor_entities.face import FaceArea
from scripts.reactor_entities.rect import Rect


colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
    (128, 0, 0),
    (0, 128, 0),
    (128, 128, 0),
    (0, 0, 128),
    (0, 128, 128),
]

def color_generator(colors):
    while True:
        for color in colors:
            yield color


def process_face_image(
        face: FaceArea,
        **kwargs,
    ) -> Image:
        image = np.array(face.image)
        overlay = image.copy()
        color_iter = color_generator(colors)
        cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), next(color_iter), -1)
        l, t, r, b = face.face_area_on_image
        cv2.rectangle(overlay, (l, t), (r, b), (0, 0, 0), 10)
        if face.landmarks_on_image is not None:
            for landmark in face.landmarks_on_image:
                cv2.circle(overlay, (int(landmark.x), int(landmark.y)), 6, (0, 0, 0), 10)
        alpha = 0.3
        output = cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0)
        
        return Image.fromarray(output)


def apply_face_mask(swapped_image:np.ndarray,target_image:np.ndarray,target_face,entire_mask_image:np.array)->np.ndarray:
    logger.status("Correcting Face Mask")
    mask_generator =  BiSeNetMaskGenerator()
    face = FaceArea(target_image,Rect.from_ndarray(np.array(target_face.bbox)),1.6,512,"")
    face_image = np.array(face.image)
    process_face_image(face)
    face_area_on_image = face.face_area_on_image
    mask = mask_generator.generate_mask(
        face_image,
        face_area_on_image=face_area_on_image,
        affected_areas=["Face"],
        mask_size=0,
        use_minimal_area=True
    )
    mask = cv2.blur(mask, (12, 12))
    # """entire_mask_image = np.zeros_like(target_image)"""
    larger_mask = cv2.resize(mask, dsize=(face.width, face.height))
    entire_mask_image[
        face.top : face.bottom,
        face.left : face.right,
    ] = larger_mask
   
    result = Image.composite(Image.fromarray(swapped_image),Image.fromarray(target_image), Image.fromarray(entire_mask_image).convert("L"))
    return np.array(result)


def rotate_array(image: np.ndarray, angle: float) -> np.ndarray:
    if angle == 0:
        return image

    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))


def rotate_image(image: Image, angle: float) -> Image:
    if angle == 0:
        return image
    return Image.fromarray(rotate_array(np.array(image), angle))


def correct_face_tilt(angle: float) -> bool:
    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
    return angle > 40


def _dilate(arr: np.ndarray, value: int) -> np.ndarray:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (value, value))
    return cv2.dilate(arr, kernel, iterations=1)


def _erode(arr: np.ndarray, value: int) -> np.ndarray:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (value, value))
    return cv2.erode(arr, kernel, iterations=1)


def dilate_erode(img: Image.Image, value: int) -> Image.Image:
    """
    The dilate_erode function takes an image and a value.
    If the value is positive, it dilates the image by that amount.
    If the value is negative, it erodes the image by that amount.

    Parameters
    ----------
        img: PIL.Image.Image
            the image to be processed
        value: int
            kernel size of dilation or erosion

    Returns
    -------
        PIL.Image.Image
            The image that has been dilated or eroded
    """
    if value == 0:
        return img

    arr = np.array(img)
    arr = _dilate(arr, value) if value > 0 else _erode(arr, -value)

    return Image.fromarray(arr)

def mask_to_pil(masks, shape: tuple[int, int]) -> list[Image.Image]:
    """
    Parameters
    ----------
    masks: torch.Tensor, dtype=torch.float32, shape=(N, H, W).
        The device can be CUDA, but `to_pil_image` takes care of that.

    shape: tuple[int, int]
        (width, height) of the original image
    """
    n = masks.shape[0]
    return [to_pil_image(masks[i], mode="L").resize(shape) for i in range(n)]

def create_mask_from_bbox(
    bboxes: list[list[float]], shape: tuple[int, int]
) -> list[Image.Image]:
    """
    Parameters
    ----------
        bboxes: list[list[float]]
            list of [x1, y1, x2, y2]
            bounding boxes
        shape: tuple[int, int]
            shape of the image (width, height)

    Returns
    -------
        masks: list[Image.Image]
        A list of masks

    """
    masks = []
    for bbox in bboxes:
        mask = Image.new("L", shape, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle(bbox, fill=255)
        masks.append(mask)
    return masks
