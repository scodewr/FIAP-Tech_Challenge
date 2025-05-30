from typing import List
from app.application.ports.input.embrapa.importation_port_in import ImportationPortIn
from app.domain.services.embrapa.importation_service import ImportationService
from pydantic import BaseModel

class ImportationAdapterIn(ImportationPortIn):
    """
    Adapter para interagir com o serviço de produção.
    """

    def __init__(self, service: ImportationService):
        self.service = service

    def get_importation_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Implementação da porta para obter os dados de produção paginados.
        """
        return self.service.get_importation_data(url=url, page=page, page_size=page_size)