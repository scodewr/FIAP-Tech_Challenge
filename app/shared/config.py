import os
from dotenv import load_dotenv

# Carrega o arquivo .env com base no ambiente
env = os.getenv("ENV", "development").lower()
if env == "production":
    load_dotenv(".env/.prod")
else:
    load_dotenv(".env/.dev")

class Settings:
    """
    Configurações globais da aplicação.
    """
    APP_TITLE = os.getenv("APP_TITLE", "Vitivinicultura API")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "API para retorno de dados sobre vitivinicultura do estado do Rio Grande do Sul.")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    CACHE_FOLDER = os.getenv("CACHE_FOLDER", "resources/cache")
    CACHE_MAX_DAYS = int(os.getenv("CACHE_MAX_DAYS", 30))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))

    # Configuração do Circuit Breaker
    BREAKER_FAIL_MAX = int(os.getenv("BREAKER_FAIL_MAX", 3))
    BREAKER_RESET_TIMEOUT = int(os.getenv("BREAKER_RESET_TIMEOUT", 10))

settings = Settings()