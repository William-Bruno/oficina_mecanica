from pathlib import Path
import yaml
from app.core.error import ConfigError

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "config.yaml"

try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as arquivo:
        config = yaml.safe_load(arquivo)
except (OSError, yaml.YAMLError) as erro:
    raise ConfigError(f"Problema ao ler o config.yaml: {erro}") from erro