app_title = "ReActor Force"
version_flag = "v0.4.2-b2"

from scripts.rf_logger import logger, get_Run, set_Run

is_run = get_Run()

if not is_run:
    logger.info(f"Running {version_flag}")
    set_Run(True)
