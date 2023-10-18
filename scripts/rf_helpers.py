import os
from collections import Counter
from PIL import Image
from math import isqrt, ceil
from typing import List
import logging

from modules.images import FilenameGenerator, get_next_sequence_number
from modules import shared, script_callbacks

def make_grid(image_list: List):
    
    # Count the occurrences of each image size in the image_list
    size_counter = Counter(image.size for image in image_list)
    
    # Get the most common image size (size with the highest count)
    common_size = size_counter.most_common(1)[0][0]
    
    # Filter the image_list to include only images with the common size
    image_list = [image for image in image_list if image.size == common_size]
    
    # Get the dimensions (width and height) of the common size
    size = common_size
    
    # If there are more than one image in the image_list
    if len(image_list) > 1:
        num_images = len(image_list)
        
        # Calculate the number of rows and columns for the grid
        rows = isqrt(num_images)
        cols = ceil(num_images / rows)

        # Calculate the size of the square image
        square_size = (cols * size[0], rows * size[1])

        # Create a new RGB image with the square size
        square_image = Image.new("RGB", square_size)

        # Paste each image onto the square image at the appropriate position
        for i, image in enumerate(image_list):
            row = i // cols
            col = i % cols

            square_image.paste(image, (col * size[0], row * size[1]))

        # Return the resulting square image
        return square_image
    
    # Return None if there are no images or only one image in the image_list
    return None

def get_image_path(image, path, basename, seed=None, prompt=None, extension='png', p=None, suffix=""):
    
    namegen = FilenameGenerator(p, seed, prompt, image)

    save_to_dirs = shared.opts.save_to_dirs

    if save_to_dirs:
        dirname = namegen.apply(shared.opts.directories_filename_pattern or "[prompt_words]").lstrip(' ').rstrip('\\ /')
        path = os.path.join(path, dirname)

    os.makedirs(path, exist_ok=True)

    if seed is None:
        file_decoration = ""
    elif shared.opts.save_to_dirs:
        file_decoration = shared.opts.samples_filename_pattern or "[seed]"
    else:
        file_decoration = shared.opts.samples_filename_pattern or "[seed]-[prompt_spaces]"

    file_decoration = namegen.apply(file_decoration) + suffix

    add_number = shared.opts.save_images_add_number or file_decoration == ''

    if file_decoration != "" and add_number:
        file_decoration = f"-{file_decoration}"

    if add_number:
        basecount = get_next_sequence_number(path, basename)
        fullfn = None
        for i in range(500):
            fn = f"{basecount + i:05}" if basename == '' else f"{basename}-{basecount + i:04}"
            fullfn = os.path.join(path, f"{fn}{file_decoration}.{extension}")
            if not os.path.exists(fullfn):
                break
    else:
        fullfn = os.path.join(path, f"{file_decoration}.{extension}")

    pnginfo = {}

    params = script_callbacks.ImageSaveParams(image, p, fullfn, pnginfo)
    # script_callbacks.before_image_saved_callback(params)

    fullfn = params.filename

    fullfn_without_extension, extension = os.path.splitext(params.filename)
    if hasattr(os, 'statvfs'):
        max_name_len = os.statvfs(path).f_namemax
        fullfn_without_extension = fullfn_without_extension[:max_name_len - max(4, len(extension))]
        params.filename = fullfn_without_extension + extension
        fullfn = params.filename

    return fullfn

def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)
