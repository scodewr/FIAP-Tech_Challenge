from typing import List
from app.application.ports.input.embrapa.processing_port_in import ProcessingPortIn
from app.domain.services.embrapa.processing_service import ProcessingService
from pydantic import BaseModel

class ProcessingAdapterIn(ProcessingPortIn):
    """
    Adapter para interagir com o serviço de produção.
    """

    def __init__(self, service: ProcessingService):
        self.service = service

    def get_processing_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Implementação da porta para obter os dados de produção paginados.
        """
        return self.service.get_processing_data(url=url, page=page, page_size=page_size)