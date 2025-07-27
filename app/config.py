# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_host: str               = Field(..., env="DB_HOST")
    db_port: int               = Field(..., env="DB_PORT")
    db_name: str               = Field(..., env="DB_NAME")
    db_user: str               = Field(..., env="DB_USER")
    db_password: str           = Field(..., env="DB_PASSWORD")

    secret_key: str            = Field(..., env="SECRET_KEY")
    algorithm: str             = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    environment: str           = Field("development", env="ENVIRONMENT")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"          # silence any variables you forgot to model
    )

settings = Settings()



# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DATABASE_HOSTNAME: str
#     DATABASE_PORT: str
#     DATABASE_PASSWORD: str
#     DATABASE_NAME: str
#     DATABASE_USERNAME: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         env_file = ".env"

# settings = Settings()