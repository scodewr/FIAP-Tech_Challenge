from fastapi import APIRouter, Query, Depends
from app.application.ports.input.embrapa.production_port_in import ProductionPortIn
from app.shared.dependencies import get_production_adapter_in, get_jwt_adapter_out
from app.domain.models.entities.embrapa.production import ProductionEntity
from fastapi.security import HTTPBearer
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from typing import List

router = APIRouter(
    prefix="/info/production",
    tags=["Informações de Produção"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    response_model=List[ProductionEntity],
    responses={
        503: {
            "description": "Erro no serviço da Embrapa.",
            "content": {
                "application/json": {
                    "example": {
                        "error": True,
                        "message": "Serviço Embrapa indisponível. Tente novamente mais tarde.",
                        "status_code": 503
                    }
                }
            },
        },
    },
)
async def info_production(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ProductionPortIn = Depends(get_production_adapter_in),
    auth_port: JWTAuthPort = Depends(get_jwt_adapter_out)
):
    #await auth_port.validate_token(endpoint_permission="info_production")
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
    data = port_in.get_production_data(url=url, page=page, page_size=page_size)
    return data