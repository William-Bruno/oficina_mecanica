import logging
import logging.config
from app.core.config_loader import BASE_DIR, config

NOME_SISTEMA = config["app"]["name"]

# Resolve os caminhos das pastas a partir do YAML
LOG_SISTEMA_PATH = BASE_DIR / config["paths"]["log_sistema_path"]
LOG_BANCO_PATH = BASE_DIR / config["paths"]["log_banco_path"]

# Garante a criação de ambas as pastas (logs/sistema e logs/banco)
LOG_SISTEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_BANCO_PATH.parent.mkdir(parents=True, exist_ok=True)

# Atualiza os filenames dos handlers no dicionário vindo do YAML
logging_config = config["logging"]
logging_config["handlers"]["file_sistema"]["filename"] = str(LOG_SISTEMA_PATH)
logging_config["handlers"]["file_banco"]["filename"] = str(LOG_BANCO_PATH)

# Renomeia o logger 'app' para o nome do sistema ("OFICINA MECANICA")
logging_config["loggers"][NOME_SISTEMA] = logging_config["loggers"].pop("app")

# Aplica a configuração do YAML
logging.config.dictConfig(logging_config)

# 🟢 Garante que APENAS o executor de queries fique em INFO
logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.INFO)

# Silencia inicializadores internos de relacionamentos e mappers
logging.getLogger("sqlalchemy.orm").setLevel(logging.WARNING)

logger = logging.getLogger(NOME_SISTEMA)