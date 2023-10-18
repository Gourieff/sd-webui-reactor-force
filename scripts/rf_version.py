app_title = "ReActor Force"
version_flag = "v0.4.3-b2"

from scripts.rf_logger import logger, get_Run, set_Run

is_run = get_Run()

if not is_run:
    logger.status(f"Running {version_flag} with CUDA support")
    set_Run(True)
