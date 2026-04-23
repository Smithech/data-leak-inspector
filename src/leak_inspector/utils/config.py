from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List, Optional

class AppConfig(BaseSettings):
    app_dir: Path = Path.home() / ".data_leak_inspector"

    accounts_dir: Optional[Path] = None
    logs_dir: Optional[Path] = None
    database_path: Optional[Path] = None
    credentials_path: Optional[Path] = None
    log_file: Optional[Path] = None

    scan_file_types: List[str] = ["txt"]

    log_level: str = "INFO"
    auto_fix_permissions: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    def model_post_init(self, __context):
        self.accounts_dir = self.app_dir / "accounts"
        self.logs_dir = self.app_dir / "logs"
        self.credentials_path = self.app_dir / "credentials.json"
        self.database_path = self.app_dir / "data.db"
        self.log_file = self.logs_dir / "app.log"

        # Create directories
        self.app_dir.mkdir(exist_ok=True)
        self.accounts_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)


config = AppConfig()