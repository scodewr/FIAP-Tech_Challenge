from app.domain.services.embrapa.production_service import ProductionService
from app.infrastructure.adapters.input.embrapa.production_adapter_in import ProductionAdapterIn
from app.infrastructure.adapters.output.embrapa.embrapa_adapter_out import EmbrapaAdapterOut
from app.infrastructure.adapters.input.iam.auth.jwt_auth_adapter_in import JWTAuthAdapterIn
from app.infrastructure.adapters.output.dataprocessing.cache_adapter_out import CacheAdapterOut
from app.application.ports.output.dataprocessing.csv_port_out import CSVPortOut
from app.domain.services.embrapa.embrapa_service import EmbrapaService
from app.domain.services.iam.auth.permissions_service import PermissionsService
from app.infrastructure.adapters.output.dataprocessing.csv_adapter_out import CSVAdapterOut
from app.domain.services.dataprocessing.csv_service import CSVService
from app.domain.services.dataprocessing.cache_service import CacheService
from app.application.ports.output.dataprocessing.cache_port_out import CachePortOut
from app.domain.services.embrapa.processing_service import ProcessingService
from app.infrastructure.adapters.input.embrapa.processing_adapter_in import ProcessingAdapterIn
from app.domain.services.embrapa.marketing_service import MarketingService
from app.infrastructure.adapters.input.embrapa.marketing_adapter_in import MarketingAdapterIn
from app.domain.services.embrapa.importation_service import ImportationService
from app.infrastructure.adapters.input.embrapa.importation_adapter_in import ImportationAdapterIn
from app.domain.services.embrapa.exportation_service import ExportationService
from app.infrastructure.adapters.input.embrapa.exportation_adapter_in import ExportationAdapterIn
from app.infrastructure.adapters.input.iam.sign_up_adater_in import SignUpAdapterIn
from app.domain.services.iam.sign_up_service import SignUpService
from app.domain.services.iam.db.local_db_service import LocalDbService
from app.application.ports.output.iam.sign_up_port_out import SignUpPortOut
from app.infrastructure.adapters.output.iam.sign_up_adapter_out import SignUpAdapterOut
from app.infrastructure.adapters.output.iam.db.local_db_adapter_out import LocalDbAdapterOut
from app.application.ports.output.iam.db.local_db_port_out import LocalDBPortOut
from app.domain.services.iam.auth.jwt_auth_service import JWTAuthService
from app.application.ports.output.iam.auth.permissions_port_out import PermissionsPortOut
from app.application.ports.input.iam.auth.jwt_auth_port_in import JWTAuthPortIn
from app.domain.services.iam.log_in_service import LogInService
from app.infrastructure.adapters.input.iam.log_in_adapter_in import LogInAdapterIn

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

def get_processing_service(embrapa_adapter: EmbrapaAdapterOut = Depends(get_embrapa_adapter)) -> ProcessingService:
    return ProcessingService(embrapa_port=embrapa_adapter)

def get_processing_adapter_in(processing_service: ProcessingService = Depends(get_processing_service)) -> ProcessingAdapterIn:
    return ProcessingAdapterIn(service=processing_service)

def get_marketing_service(embrapa_adapter: EmbrapaAdapterOut = Depends(get_embrapa_adapter)) -> MarketingService:
    return MarketingService(embrapa_port=embrapa_adapter)

def get_marketing_adapter_in(marketing_service: MarketingService = Depends(get_marketing_service)) -> MarketingAdapterIn:
    return MarketingAdapterIn(service=marketing_service)

def get_importation_service(embrapa_adapter: EmbrapaAdapterOut = Depends(get_embrapa_adapter)) -> ImportationService:
    return ImportationService(embrapa_port=embrapa_adapter)

def get_importation_adapter_in(importation_service: ImportationService = Depends(get_importation_service)) -> ImportationAdapterIn:
    return ImportationAdapterIn(service=importation_service)

def get_exportation_service(embrapa_adapter: EmbrapaAdapterOut = Depends(get_embrapa_adapter)) -> ExportationService:
    return ExportationService(embrapa_port=embrapa_adapter)

def get_exportation_adapter_in(exportation_service: ExportationService = Depends(get_exportation_service)) -> ExportationAdapterIn:
    return ExportationAdapterIn(service=exportation_service)

def get_local_db_service() -> LocalDbService:
    return LocalDbService()

def get_sign_up_adapter_out(service: LocalDbService = Depends(get_local_db_service)) -> SignUpAdapterOut:
    return SignUpAdapterOut(service=service)

def get_sign_up_service(port_out: SignUpPortOut = Depends(get_sign_up_adapter_out)) -> SignUpService:
    return SignUpService(port_out=port_out)

def get_sign_up_adapter_in(service: SignUpService = Depends(get_sign_up_service)) -> SignUpAdapterIn:
    return SignUpAdapterIn(service=service)


def get_local_db_adapter_out(service: LocalDbService = Depends(get_local_db_service)) -> LocalDbAdapterOut:
    return LocalDbAdapterOut(service=service)

def get_permissions_adapter_out(local_db_port: LocalDBPortOut = Depends(get_local_db_adapter_out)) -> PermissionsService:
    return PermissionsService(local_db_port=local_db_port)

def get_jwt_service(permission_port_out: PermissionsPortOut = Depends(get_permissions_adapter_out)) -> JWTAuthService:
    return JWTAuthService(permissions_port_out=permission_port_out)

def get_jwt_adapter_in(service: JWTAuthService = Depends(get_jwt_service)) -> JWTAuthAdapterIn:
    return JWTAuthAdapterIn(service=service)

def get_log_in_service(permissions_port_out: PermissionsPortOut = Depends(get_permissions_adapter_out), token_port_in: JWTAuthPortIn = Depends(get_jwt_adapter_in)) -> LogInService:
    return LogInService(permissions_port_out=permissions_port_out, token_port_in=token_port_in)

def get_log_in_adapter_in(service: LogInService = Depends(get_log_in_service)) -> LogInAdapterIn:
    return LogInAdapterIn(service=service)