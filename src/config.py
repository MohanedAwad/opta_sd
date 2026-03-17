import os
from pathlib import Path
from typing import Optional
from dotenv import dotenv_values

from .exceptions import ConfigurationError


def load_config(config_path: Optional[str | Path] = None) -> dict:
    file_config: dict = {}

    if config_path:
        path = Path(config_path).expanduser()
        if path.exists():
            file_config = dotenv_values(path) or {}

    opta_domain = os.environ.get("OPTA_DOMAIN") or file_config.get("OPTA_DOMAIN") or file_config.get("opta_domain")
    token  = os.environ.get("OPTA_AUTH_TOKEN") or file_config.get("OPTA_AUTH_TOKEN") or file_config.get("opta_auth_token")
    referer_domain = os.environ.get("REFERER_DOMAIN") or file_config.get("REFERER_DOMAIN") or file_config.get("referer_domain")


    if not opta_domain:
        raise ConfigurationError(
            "OPTA domain not set.  Supply the OPTA_DOMAIN environment variable "
            "or 'opta_domain' in your config YAML."
        )
    if not token:
        raise ConfigurationError(
            "OPTA auth token not set.  Supply the OPTA_AUTH_TOKEN environment "
            "variable or 'opta_auth_token' in your config YAML."
        )

    return {"opta_domain": opta_domain.rstrip("/"), "opta_auth_token": token, "referer_domain": referer_domain}