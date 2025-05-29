from typing import Type, List
from app.application.ports.input.production_port_in import ProductionPortIn
from app.domain.services.embrapa.production_service import ProductionService
from pydantic import BaseModel

class ProductionAdapterIn(ProductionPortIn):
    """
    Adapter para interagir com o serviço de produção.
    """

    def __init__(self, service: ProductionService):
        self.service = service

    def get_production_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Implementação da porta para obter os dados de produção paginados.
        """
        return self.service.get_production_data(url=url, page=page, page_size=page_size)