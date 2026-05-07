from pathlib import Path
from typing import List

import toml
from pydantic import Field
from pydantic_settings import BaseSettings
from platformdirs import user_config_dir, user_data_dir


APP_NAME = "dli"
APP_AUTHOR = "leak_inspector"


# -------------------------
# Paths (no user config)
# -------------------------
class AppPaths:
    def __init__(self):
        self.config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
        self.data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))

        self.config_file = self.config_dir / "config.toml"

        self.credentials_path = self.config_dir / "credentials.json"
        self.token_path = self.data_dir / "token.json"


# -------------------------
# User Settings (editable)
# -------------------------
class Settings(BaseSettings):
    # Google
    google_credentials_path: Path
    google_token_path: Path

    # App config
    database_path: Path
    reports_dir: Path
    allowed_extensions: List[str] = Field(default_factory=lambda: [".pdf", ".docx", ".txt"])

    class Config:
        arbitrary_types_allowed = True


# -------------------------
# Defaults
# -------------------------
def default_settings(paths: AppPaths) -> dict:
    return {
        "google_credentials_path": str(paths.credentials_path),
        "google_token_path": str(paths.token_path),
        "database_path": str(paths.data_dir / "scans.db"),
        "reports_dir": str(paths.data_dir / "reports"),
        #"allowed_extensions": [".pdf", ".docx", ".txt"],
    }


# -------------------------
# Load / Create config
# -------------------------
def load_settings() -> Settings:
    paths = AppPaths()

    paths.config_dir.mkdir(parents=True, exist_ok=True)
    paths.data_dir.mkdir(parents=True, exist_ok=True)

    if not paths.config_file.exists():
        config_data = default_settings(paths)

        with open(paths.config_file, "w") as f:
            toml.dump(config_data, f)

    else:
        config_data = toml.load(paths.config_file)

    return Settings(**config_data)