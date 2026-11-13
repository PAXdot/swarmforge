from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Optional
import json
import yaml

def validate_backoff_config(backoff_config: Dict[str, Any]) -> None:
    """
    Validate the backoff configuration, ensuring it contains 'strategy', 'initial' and 'max' values.

    :param backoff_config: The backoff configuration dictionary.
    :raises ValueError: If the configuration is invalid.
    """
    if 'strategy' not in backoff_config or 'initial' not in backoff_config or 'max' not in backoff_config:
        raise ValueError("Backoff configuration must contain 'strategy', 'initial' and 'max' fields.")

def load_consensus_config(config_file: str) -> Dict[str, Any]:
    """
    Load consensus configuration from a JSON or YAML file.

    :param config_file: Path to the configuration file.
    :return: The loaded configuration as a dictionary.
    :raises ValueError: If the file doesn't exist, has invalid format, or contains invalid backoff configuration.
    """
    file_path = Path(config_file)

    if not file_path.is_file():
        raise ValueError(f"Configuration file '{config_file}' does not exist.")

    if file_path.suffix in ('.json', '.yml', '.yaml'):
        with open(file_path, 'r') as f:
            if file_path.suffix == '.yml':
                config = yaml.safe_load(f)
            else:
                config = json.load(f)

        validate_backoff_config(config.get('backoff', {}))  # Validate backoff configuration if present
        return config
    else:
        raise ValueError(f"Unsupported file format. Must be JSON or YAML. Got '{file_path.suffix}'")
