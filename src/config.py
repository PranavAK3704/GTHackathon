from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(path: str | Path = "config.yaml") -> Dict[str, Any]:
    """
    Load YAML configuration file.

    Parameters
    ----------
    path : str | Path
        Path to the config.yaml file.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration dictionary.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
