from typing import List, Type, Optional
from enum import Enum
from app.application.ports.output.csv_port_out import CSVPortOut
from app.domain.services.dataprocessing.csv_service import CSVService
from pydantic import BaseModel

class CSVAdapterOut(CSVPortOut):
    """
    Adapter para interagir com arquivos CSV.
    """

    def __init__(self, service: CSVService):
        self.service = service

    def process_csv(
        self,
        file_path: str,
        model: Type[BaseModel],
        category_enum: Optional[Type[Enum]] = None,
        value_name_column: str = "production",
        delimiter: str = ";"
    ) -> List[BaseModel]:
        """
        Implementação da porta para processar os dados de um arquivo CSV.
        """
        return self.service.process_csv_data(
            file_path=file_path,
            model=model,
            category_enum=category_enum,
            value_name_column=value_name_column,
            delimiter=delimiter
        )