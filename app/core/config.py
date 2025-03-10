import json
from typing import cast

from dotenv import load_dotenv
from pydantic import validator
from pydantic_settings import BaseSettings  # type: ignore

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings.

    This class loads settings from environment variables and the .env file.
    """

    # Application settings
    APP_NAME: str = "FastAPI Hexagonal"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "development-secret-key-change-in-production"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db_name"

    # Authentication
    JWT_SECRET_KEY: str = "jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        """Convert ALLOWED_HOSTS from various formats to a list of strings.

        Args:
            v: The value to convert, which can be a comma-separated string,
               a JSON string representing a list, or already a list.

        Returns:
            list[str]: List of allowed hosts
        """
        if isinstance(v, str) and not v.startswith("["):
            # Handle comma-separated string
            return [host.strip() for host in v.split(",")]
        elif isinstance(v, str):
            # Handle JSON string
            try:
                hosts = json.loads(v)
                return cast(list[str], hosts)
            except json.JSONDecodeError:
                return [v]
        return cast(list[str], v)

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
