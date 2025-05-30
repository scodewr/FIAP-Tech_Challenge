from typing import Type, List
from app.domain.models.entities.embrapa.exportation import ExportationEntity
from pydantic import BaseModel

class ExportationPortIn:
    """
    Interface para abstrair os casos de uso relacionados à produção.
    """

    def get_exportation_data(self, url: str, model: Type[ExportationEntity], page: int, page_size: int) -> List[BaseModel]:
        """
        Obtém os dados de produção paginados.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados.
        :param page: Número da página.
        :param page_size: Tamanho da página.
        :return: Lista de instâncias do modelo.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")