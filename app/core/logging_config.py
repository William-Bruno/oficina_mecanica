import logging
import logging.config
from app.core.config_loader import config, BASE_DIR

NOME_SISTEMA = config["app"]["name"]

LOG_PATH = BASE_DIR / config["paths"]["log_path"]
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging_config = config["logging"]
logging_config["handlers"]["file"]["filename"] = str(LOG_PATH)
logging_config["loggers"][NOME_SISTEMA] = logging_config["loggers"].pop("app")
logging.config.dictConfig(logging_config)

logger = logging.getLogger(NOME_SISTEMA)