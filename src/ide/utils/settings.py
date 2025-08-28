from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import BaseModel, Field
from functools import lru_cache

class AplicacionSettings(BaseSettings):
    # Global settings for the application
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    reload: bool = Field(False, env="RELOAD")
    
    # Kubernetes settings
    namespace: str = Field("ide-namespace", env="NAMESPACE")
    max_allowed_lifetime_seconds: int = Field(3600, env="MAX_ALLOWED_LIFETIME_SECONDS")
    pod_container_image: str = Field("code-server:latest", env="POD_CONTAINER_IMAGE")
    pod_container_port: int = Field(8080, env="POD_CONTAINER_PORT")


    # API settings
    api_port: int = Field(8000, env="API_PORT")
    api_prefix: str = Field("/api/v1", env="API_PREFIX")

    
    class Config:
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_config() -> AplicacionSettings:
    return AplicacionSettings()

settings = AplicacionSettings()
