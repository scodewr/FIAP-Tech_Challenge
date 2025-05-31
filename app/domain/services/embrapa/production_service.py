from typing import List
from app.application.ports.output.embrapa.embrapa_port_out import EmbrapaPortOut
from pydantic import BaseModel
from app.domain.models.entities.embrapa.production import ProductionEntity, ProductionCategoryEnum

class ProductionService:
    """
    Serviço para lógica de negócio relacionada à produção.
    """

    def __init__(self, embrapa_port: EmbrapaPortOut):
        self.embrapa_port = embrapa_port

    def get_production_data(self, url: str, page: int, page_size: int) -> List[BaseModel]:
        """
        Obtém os dados de produção paginados.

        :param url: URL da página da Embrapa.
        :param model: Modelo para mapear os dados.
        :param page: Número da página.
        :param page_size: Tamanho da página.
        :return: Lista de instâncias do modelo.
        """
        # Faz o download do CSV usando o portOut da Embrapa
        csv_data = self.embrapa_port.get_csv_data(url=url, model=ProductionEntity, category_enum=ProductionCategoryEnum, value_name_column="production", delimiter=";")

        # Processa os dados (simulação de lógica de processamento)
        processed_data = [ProductionEntity(**row) for row in csv_data.to_dict(orient="records")]

        # Paginação
        start = (page - 1) * page_size
        end = start + page_size
        return processed_data[start:end]