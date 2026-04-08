from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Try .env first; fall back to .env.example if .env is absent.
        env_file=(".env.example", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        # Raise ValidationError immediately on missing required fields.
        extra="ignore",
    )

    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Required — no defaults. Missing values raise ValidationError at import time.
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    GEMINI_API_KEY: str


settings = Settings()
