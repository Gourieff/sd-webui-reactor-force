'''
Thanks @ledahu for contributing
'''

from modules import scripts
from modules.shared import opts

from scripts.reactor_helpers import (
    get_model_names, 
    get_facemodels
)


# xyz_grid = [x for x in scripts.scripts_data if x.script_class.__module__ == "xyz_grid.py"][0].module

def find_module(module_names):
    if isinstance(module_names, str):
        module_names = [s.strip() for s in module_names.split(",")]
    for data in scripts.scripts_data:
        if data.script_class.__module__ in module_names and hasattr(data, "module"):
            return data.module
    return None

def bool_(string):
    string = str(string)
    if string in ["None", ""]:
        return None
    elif string.lower() in ["true", "1"]:
        return True
    elif string.lower() in ["false", "0"]:
        return False
    else:
        raise ValueError(f"Could not convert string to boolean: {string}")

def choices_bool():
    return ["False", "True"]

def choices_face_models():
    return get_model_names(get_facemodels)

def float_applier(value_name:str, min_range:float = 0, max_range:float = 1):
    """
    Returns a function that applies the given value to the given value_name in opts.data.
    """
    def validate(value_name:str, value:str):
        value = float(value)
        # validate value
        if not min_range == 0:
            assert value >= min_range, f"Value {value} for {value_name} must be greater than or equal to {min_range}"
        if not max_range == 1:
            assert value <= max_range, f"Value {value} for {value_name} must be less than or equal to {max_range}"
    def apply_float(p, x, xs):
        validate(value_name, x)
        opts.data[value_name] = float(x)
    return apply_float

def bool_applier(value_name:str):
    def apply_bool(p, x, xs):
        x_normed = bool_(x)
        opts.data[value_name] = x_normed
        # print(f'normed = {x_normed}')
    return apply_bool

def str_applier(value_name:str):
    def apply_str(p, x, xs):
        opts.data[value_name] = x
    return apply_str


def add_axis_options(xyz_grid):
    extra_axis_options = [
        xyz_grid.AxisOption("[ReActor] CodeFormer Weight", float, float_applier("codeformer_weight", 0, 1)),
        xyz_grid.AxisOption("[ReActor] Restorer Visibility", float, float_applier("restorer_visibility", 0, 1)),
        xyz_grid.AxisOption("[ReActor] Face Mask Correction", str, bool_applier("mask_face"), choices=choices_bool),
        xyz_grid.AxisOption("[ReActor] Face Models", str, str_applier("face_model"), choices=choices_face_models),
    ]
    set_a = {opt.label for opt in xyz_grid.axis_options}
    set_b = {opt.label for opt in extra_axis_options}
    if set_a.intersection(set_b):
        return

    xyz_grid.axis_options.extend(extra_axis_options)

def run():
    xyz_grid = find_module("xyz_grid.py, xy_grid.py")
    if xyz_grid:
        add_axis_options(xyz_grid)

# XYZ init:
try:
    import modules.script_callbacks as script_callbacks
    script_callbacks.on_before_ui(run)
except:
    pass
