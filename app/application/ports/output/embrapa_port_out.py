from typing import Optional, Type
from enum import Enum
from pydantic import BaseModel
import pandas as pd

class EmbrapaPortOut:
    """
    Interface para abstrair as interações com o sistema da Embrapa.
    """
    def get_csv_data(self, url: str, model: Type[BaseModel], category_enum: Optional[Type[Enum]] = None, value_name_column: str = "production", delimiter: str = ";") -> pd.DataFrame:
        """
        Obtém e processa os dados do arquivo CSV da Embrapa.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados do CSV.
        :param delimiter: Delimitador do CSV (padrão: ";").
        :return: Caminho do arquivo CSV processado.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")