import os
import hashlib
import pandas as pd
from app.shared.config import settings
from datetime import datetime, timedelta

class CacheService:
    """
    Serviço para manipulação de cache.
    """

    def save_csv_to_cache(self, url: str, df: pd.DataFrame) -> str:
        """
        Salva um DataFrame como um arquivo CSV no cache.

        :param url: URL do CSV.
        :param df: DataFrame a ser salvo.
        :return: Caminho completo do arquivo salvo.
        """
        file_hash = hashlib.md5(url.encode()).hexdigest()
        file_path = os.path.join(settings.CACHE_FOLDER, f"{file_hash}.csv")
        os.makedirs(settings.CACHE_FOLDER, exist_ok=True)
        df.to_csv(file_path, index=False, encoding="utf-8", sep=";")
        return file_path

    def get_csv_file_path(self, url: str) -> str:
        """
        Retorna o caminho do arquivo CSV no cache com base na URL.

        :param url: URL do CSV.
        :return: Caminho completo do arquivo no cache.
        """
        file_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(settings.CACHE_FOLDER, f"{file_hash}.csv")

    def is_file_in_cache(self, file_path: str) -> bool:
        """
        Verifica se o arquivo existe no cache.

        :param file_path: Caminho do arquivo.
        :return: True se o arquivo existir, False caso contrário.
        """
        return os.path.exists(file_path)

    

    def is_cache_expired(self, file_path: str, max_days: int = 30) -> bool:
        """
        Verifica se um arquivo em cache tem mais de `max_days` dias.

        :param file_path: Caminho para o arquivo.
        :param max_days: Dias máximos permitidos antes do cache expirar.
        :return: True se o cache expirou, False caso contrário.
        """
        if not os.path.exists(file_path):
            return True  # Arquivo não existe = expirado

        file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        expiration_time = datetime.now() - timedelta(days=settings.CACHE_MAX_DAYS)
        
        return file_mod_time < expiration_time
