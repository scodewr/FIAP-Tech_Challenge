from app.application.ports.output.embrapa.embrapa_port_out import EmbrapaPortOut
from app.domain.services.embrapa.embrapa_service import EmbrapaService
from typing import Type, Optional
from pydantic import BaseModel
import pandas as pd
from enum import Enum

class EmbrapaAdapterOut(EmbrapaPortOut):
    """
    Adapter para interagir com o sistema da Embrapa.
    """

    def __init__(self, service: EmbrapaService):
        self.service = service

    def get_csv_data(self, url: str, model: Type[BaseModel], category_enum: Optional[Type[Enum]] = None, value_name_column: str = "production", delimiter: str = ";") -> pd.DataFrame:
        """
        Implementação da porta para obter e processar os dados do arquivo CSV da Embrapa.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados do CSV.
        :param delimiter: Delimitador do CSV (padrão: ";").
        :return: DataFrame com os dados do CSV.
        """
        return self.service.get_csv_data(url=url, model=model, category_enum=category_enum, value_name_column=value_name_column, delimiter=delimiter)