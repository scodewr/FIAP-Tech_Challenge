from app.domain.services.embrapa.production_service import ProductionService
from app.infrastructure.adapters.input.production_adapter_in import ProductionAdapterIn
from app.infrastructure.adapters.output.embrapa_adapter_out import EmbrapaAdapterOut
from app.infrastructure.adapters.output.auth.jwt_adapter_out import JWTAdapterOut
from app.application.ports.output.embrapa_port_out import EmbrapaPortOut
from app.infrastructure.adapters.output.cache_adapter_out import CacheAdapterOut
from app.application.ports.output.csv_port_out import CSVPortOut
from app.domain.services.embrapa.embrapa_service import EmbrapaService
from app.domain.services.auth.permissions_service import PermissionsService
from app.infrastructure.adapters.output.csv_adapter_out import CSVAdapterOut
from app.domain.services.dataprocessing.csv_service import CSVService
from app.domain.services.dataprocessing.cache_service import CacheService
from app.application.ports.output.cache_port_out import CachePortOut

from fastapi import Depends

def get_csv_adapter_out() -> CSVAdapterOut:
    return CSVAdapterOut(service=CSVService())

def get_cache_adapter_out() -> CacheAdapterOut:
    return CacheAdapterOut(service=CacheService())

def get_embrapa_service(cache_port: CachePortOut = Depends(get_cache_adapter_out), csv_port: CSVPortOut = Depends(get_csv_adapter_out)) -> EmbrapaService:
    return EmbrapaService(cache_port=cache_port, csv_port=csv_port)

def get_embrapa_adapter(embrapa_service: EmbrapaService = Depends(get_embrapa_service)) -> EmbrapaAdapterOut:
    return EmbrapaAdapterOut(service=embrapa_service) 

def get_production_service(embrapa_adapter: EmbrapaAdapterOut = Depends(get_embrapa_adapter)) -> ProductionService:
    return ProductionService(embrapa_port=embrapa_adapter)

def get_production_adapter_in(production_service: ProductionService = Depends(get_production_service)) -> ProductionAdapterIn:
    return ProductionAdapterIn(service=production_service)

def get_jwt_adapter_out() -> JWTAdapterOut:
    return JWTAdapterOut(permissions_service=PermissionsService())