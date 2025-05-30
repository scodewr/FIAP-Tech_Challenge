from typing import Type, List
from app.domain.models.entities.embrapa.marketing import MarketingEntity
from pydantic import BaseModel

class MarketingPortIn:
    """
    Interface para abstrair os casos de uso relacionados à produção.
    """

    def get_marketing_data(self, url: str, model: Type[MarketingEntity], page: int, page_size: int) -> List[BaseModel]:
        """
        Obtém os dados de produção paginados.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados.
        :param page: Número da página.
        :param page_size: Tamanho da página.
        :return: Lista de instâncias do modelo.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")