from typing import List
from app.application.ports.input.embrapa.exportation_port_in import ExportationPortIn
from app.domain.services.embrapa.exportation_service import ExportationService
from pydantic import BaseModel

class ExportationAdapterIn(ExportationPortIn):
    """
    Adapter para interagir com o serviço de produção.
    """

    def __init__(self, service: ExportationService):
        self.service = service

    def get_exportation_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Implementação da porta para obter os dados de produção paginados.
        """
        return self.service.get_exportation_data(url=url, page=page, page_size=page_size)