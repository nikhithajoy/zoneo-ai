from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    anthropic_api_key: str = ""
    google_places_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    max_tokens: int = 4096
    log_level: str = "INFO"

    places_base_url: str = "https://places.googleapis.com/v1"
    geocoding_base_url: str = "https://maps.googleapis.com/maps/api/geocode/json"


settings = Settings()
