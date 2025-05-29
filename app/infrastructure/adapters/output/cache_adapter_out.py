from app.application.ports.output.cache_port_out import CachePortOut
from app.domain.services.dataprocessing.cache_service import CacheService
import pandas as pd

class CacheAdapterOut(CachePortOut):
    """
    Adapter para interagir com o sistema de cache.
    """

    def __init__(self, service: CacheService):
        self.service = service

    def save_csv_to_cache(self, url: str, df: pd.DataFrame) -> str:
        """
        Salva um DataFrame como um arquivo CSV no cache.
        """
        return self.service.save_csv_to_cache(url, df=df)

    def get_csv_file_path(self, url: str) -> str:
        """
        Retorna o caminho do arquivo CSV no cache com base na URL.
        """
        return self.service.get_csv_file_path(url)

    def is_file_in_cache(self, file_path: str) -> bool:
        """
        Verifica se o arquivo existe no cache.
        """
        return self.service.is_file_in_cache(file_path=file_path)
    
    def is_cache_expired(self, file_path: str, max_days: int = 30) -> bool:
        """
        Verifica se um arquivo em cache tem mais de `max_days` dias.
        """
        return self.service.is_cache_expired(file_path=file_path, max_days=max_days)