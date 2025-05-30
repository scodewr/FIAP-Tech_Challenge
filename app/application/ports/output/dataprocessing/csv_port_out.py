from typing import List, Type, Optional
from enum import Enum
from pydantic import BaseModel

class CSVPortOut:
    """
    Interface para abstrair as operações relacionadas a arquivos CSV.
    """

    def process_csv(
        self,
        file_path: str,
        model: Type[BaseModel],
        category_enum: Optional[Type[Enum]] = None,
        value_name_column: str = "production",
        delimiter: str = ";"
    ) -> List[BaseModel]:
        """
        Processa os dados de um arquivo CSV e retorna uma lista de instâncias do BaseModel.

        :param file_path: Caminho do arquivo CSV.
        :param model: O BaseModel para mapear os dados.
        :param category_enum: Enum opcional para filtrar categorias.
        :param value_name_column: Nome da coluna de valores (padrão: "production").
        :param delimiter: Delimitador do CSV (padrão: ";").
        :return: Lista de instâncias do BaseModel.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")