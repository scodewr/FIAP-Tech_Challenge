from typing import List
from app.application.ports.input.embrapa.marketing_port_in import MarketingPortIn
from app.domain.services.embrapa.marketing_service import MarketingService
from pydantic import BaseModel

class MarketingAdapterIn(MarketingPortIn):
    """
    Adapter para interagir com o serviço de produção.
    """

    def __init__(self, service: MarketingService):
        self.service = service

    def get_marketing_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Implementação da porta para obter os dados de produção paginados.
        """
        return self.service.get_marketing_data(url=url, page=page, page_size=page_size)