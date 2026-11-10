from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json
import yaml

def load_consensus_config(config_file: str) -> Dict[str, Any]:
    """
    Load consensus configuration from a JSON or YAML file.

    :param config_file: Path to the configuration file.
    :return: The loaded configuration as a dictionary.
    :raises ValueError: If the file doesn't exist or has invalid format.
    """
    file_path = Path(config_file)

    if not file_path.is_file():
        raise ValueError(f"Configuration file '{config_file}' does not exist.")

    if file_path.suffix in ('.json', '.yml', '.yaml'):
        with open(file_path, 'r') as f:
            if file_path.suffix == '.yml':
                return yaml.safe_load(f)
            else:
                return json.load(f)
    else:
        raise ValueError(f"Unsupported file format. Must be JSON or YAML. Got '{file_path.suffix}'")
