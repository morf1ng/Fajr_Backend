# config.py
import urllib.parse
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "Fajr_DataBase"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_PORT: str = "5432"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_db_url():
    settings = Settings()
    encoded_password = urllib.parse.quote_plus(settings.DB_PASSWORD)
    return f"postgresql://{settings.DB_USER}:{encoded_password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

def get_db_config():
    settings = Settings()
    return {
        "host": settings.DB_HOST,
        "database": settings.DB_NAME,
        "user": settings.DB_USER,
        "password": settings.DB_PASSWORD,
        "port": settings.DB_PORT
    }