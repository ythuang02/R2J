import os
import time
import logging
import shutil

from config import cfg
from evaluate import evaluate
from finetune import finetune

logger = logging.getLogger("main")

def get_exp_name():
    return "%s_%s_%s" % (cfg["experiment"]["dataset"], cfg["model"]["target"]["model"], time.strftime(r'%Y%m%d%H%M%S'))

class ExitOnExceptionHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            exit(-1)

def setup_logging():
    if cfg["experiment"]["resume"] == False:
        result_path = os.path.join("results", get_exp_name())
        os.makedirs(result_path, exist_ok = True)
    else:
        result_path = cfg["experiment"]["resume"]

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s", 
        handlers = [
            logging.FileHandler(os.path.join(result_path, "logfile")), 
            ExitOnExceptionHandler()
        ], 
        level=logging.INFO
    )
    
    logger.info("Running experiment %s", get_exp_name())
    logger.info("Loaded configuration %s", cfg)

    return result_path

def checkpoint(step):
    logger.info("Saving checkpoint %d" % (step))
    with open(os.path.join(cfg["workspace"], "current_step"), "w") as f:
        f.write(str(step))
    
def main_loop():
    cfg["workspace"] = workspace = setup_logging()
    
    try:
        cfg["data_path"] = data_path = os.path.join(workspace, "data.json")

        if cfg["experiment"]["resume"] == False:
            shutil.copy2(os.path.join("datasets", "%s.json" % cfg["experiment"]["dataset"]), data_path)
            step = cfg["experiment"]["start_from"]
            checkpoint(step)
        else:
            if not os.path.exists(data_path):
                logger.critical("Failed to resume: %s not found" % data_path)
            if not os.path.exists(os.path.join(workspace, "current_step")):
                logger.critical("Failed to resume: %s not found" % os.path.join(workspace, "current_step"))
            
            step = int(open(os.path.join(workspace, "current_step")).read())
        
        evaluate(step - 1)

        for step in range(step, cfg["experiment"]["max_step"] + 1):
            finetune(step)
            checkpoint(step + 1)
            evaluate(step)
        
    except Exception as e:
        logger.warning(e)
        raise e