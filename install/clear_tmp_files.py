import os
import sys

intallation_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(intallation_dir))

import config
from utils import get_logger

logger = get_logger(config.LOG_PATH)

for file_ in os.listdir(config.DUMP_FOLDER_PATH):
    if file_.endswith((".zip", ".tar.gz", ".tar.bz2")):
        logger.info("[clear_tmp_files][Deleteing tmp File({})]".format(os.path.join(config.DUMP_FOLDER_PATH, file_)))
        os.remove(os.path.join(config.DUMP_FOLDER_PATH, file_))