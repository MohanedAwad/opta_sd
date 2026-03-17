import os
from pathlib import Path
from typing import Optional
from dotenv import dotenv_values

from .exceptions import ConfigurationError


def load_config(config_path: Optional[str | Path] = None) -> dict:
    file_config: dict = {}

    # Step 1: Use provided path if given
    if config_path:
        path = Path(config_path).expanduser()
        if path.exists():
            file_config = dotenv_values(path) or {}
    else:
        # Step 2: Default to project root .env
        root_path = Path(__file__).parent.parent  # adjust to repo root if needed
        default_env = root_path / ".env"
        if default_env.exists():
            file_config = dotenv_values(default_env) or {}

    # Step 3: Read environment variables first, then from file
    opta_domain = (
        os.environ.get("OPTA_DOMAIN")
        or file_config.get("OPTA_DOMAIN")
        or file_config.get("opta_domain")
    )
    token = (
        os.environ.get("OPTA_AUTH_TOKEN")
        or file_config.get("OPTA_AUTH_TOKEN")
        or file_config.get("opta_auth_token")
    )
    referer_domain = (
        os.environ.get("REFERER_DOMAIN")
        or file_config.get("REFERER_DOMAIN")
        or file_config.get("referer_domain")
    )

    # Step 4: Raise if missing
    if not opta_domain:
        raise ConfigurationError(
            "OPTA domain not set. Supply the OPTA_DOMAIN environment variable "
            "or 'opta_domain' in your .env file."
        )
    if not token:
        raise ConfigurationError(
            "OPTA auth token not set. Supply the OPTA_AUTH_TOKEN environment variable "
            "or 'opta_auth_token' in your .env file."
        )

    return {
        "opta_domain": opta_domain.rstrip("/"),
        "opta_auth_token": token,
        "referer_domain": referer_domain,
    }