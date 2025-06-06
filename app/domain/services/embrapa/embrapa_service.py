from typing import Type, Optional
import pandas as pd
from app.application.ports.output.dataprocessing.cache_port_out import CachePortOut
from app.application.ports.output.dataprocessing.csv_port_out import CSVPortOut
from pydantic import BaseModel
import requests
from starlette.exceptions import HTTPException
from bs4 import BeautifulSoup
from enum import Enum
from app.shared.config import settings
import pybreaker

class EmbrapaService:
    """
    Serviço para manipulação de dados obtidos da Embrapa.
    """

    embrapa_breaker = pybreaker.CircuitBreaker(
        fail_max=settings.BREAKER_FAIL_MAX,
        reset_timeout=settings.BREAKER_RESET_TIMEOUT
    )

    def __init__(self, cache_port: CachePortOut, csv_port: CSVPortOut):
        self.cache_port = cache_port
        self.csv_port = csv_port

    def get_csv_data(self, url: str, model: Type[BaseModel], category_enum: Optional[Type[Enum]] = None, value_name_column: str = "production", delimiter: str = ";") -> pd.DataFrame:
        """
        Obtém e processa os dados do arquivo CSV da Embrapa.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados do CSV.
        :param delimiter: Delimitador do CSV (padrão: ";").
        :return: DataFrame com os dados do CSV.
        """
        # Verifica se o arquivo está no cache
        
        cached_file_path = self.cache_port.get_csv_file_path(url=url)
        if self.cache_port.is_file_in_cache(cached_file_path) and self.cache_port.is_cache_expired(cached_file_path) is False:
            # Processa o arquivo CSV diretamente do cache
            return pd.read_csv(
                filepath_or_buffer=cached_file_path,
                delimiter=delimiter
            )

        # Faz o download do CSV
        csv_url = self.download_csv(url=url)
        
        result = self.csv_port.process_csv(
            file_path=csv_url,
            model=model,
            category_enum=category_enum,
            value_name_column=value_name_column,
            delimiter=delimiter
        )

        # Salva o arquivo no cache
        df = pd.DataFrame([item.model_dump() for item in result])
        self.cache_port.save_csv_to_cache(url=url, df=df, sep=delimiter)

        return df
    
    def download_csv(self, url: str) -> str:
        try:
            # Chamada protegida com circuit breaker
            response = self.embrapa_breaker.call(requests.get, url, timeout=10)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail="Falha ao acessar a página da Embrapa."
                )

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            link_tag = soup.find("a", href=True, text=None, class_="footer_content")

            if not link_tag or not link_tag.find("span", string=lambda s: s and "DOWNLOAD" in s.upper()):
                raise HTTPException(
                    status_code=404,
                    detail="Download link não encontrado."
                )

            download_url = link_tag["href"]
            if download_url.startswith("/"):
                download_url = "http://vitibrasil.cnpuv.embrapa.br" + download_url
            elif not download_url.startswith("http"):
                download_url = "http://vitibrasil.cnpuv.embrapa.br/" + download_url.lstrip("/")

            return download_url

        except pybreaker.CircuitBreakerError:
            raise HTTPException(
                status_code=503,
                detail="Serviço da Embrapa temporariamente indisponível (circuito aberto)."
            )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=502,
                detail=f"Erro ao conectar ao serviço da Embrapa: {str(e)}"
            )