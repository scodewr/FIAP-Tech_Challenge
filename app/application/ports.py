from typing import List, Optional
from app.domain.models import ProductionEntity, ProcessingEntity, MarketingEntity, ImportationEntity, ExportationEntity

class ProductionRepositoryPort:
    def get_production_data(self, page: int, page_size: int) -> List[ProductionEntity]:
        """
        Interface para obter dados de produção.
        """
        pass

class ProcessingRepositoryPort:
    def get_processing_data(self, page: int, page_size: int) -> List[ProcessingEntity]:
        """
        Interface para obter dados de processamento.
        """
        pass

class MarketingRepositoryPort:
    def get_marketing_data(self, page: int, page_size: int) -> List[MarketingEntity]:
        """
        Interface para obter dados de marketing.
        """
        pass

class ImportationRepositoryPort:
    def get_importation_data(self, page: int, page_size: int) -> List[ImportationEntity]:
        """
        Interface para obter dados de importação.
        """
        pass

class ExportationRepositoryPort:
    def get_exportation_data(self, page: int, page_size: int) -> List[ExportationEntity]:
        """
        Interface para obter dados de exportação.
        """
        pass