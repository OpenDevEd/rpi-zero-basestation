import sys

sys.path.append("../utils")
sys.path.append("../")
import utils

import config

# send logs to server
utils.upload_logs_files_to_api(config.SERVER_URL, config.LOG_PATH)
