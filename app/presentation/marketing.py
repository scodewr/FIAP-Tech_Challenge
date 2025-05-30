from fastapi import APIRouter, Query, Depends
from typing import List
from app.domain.models.entities.embrapa.marketing import MarketingEntity
from fastapi.security import HTTPBearer
from app.application.ports.input.embrapa.marketing_port_in import MarketingPortIn
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from app.shared.dependencies import get_jwt_adapter_out, get_marketing_adapter_in

router = APIRouter(
    prefix="/info/marketing",
    tags=["Informações de Marketing"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    response_model=List[MarketingEntity],
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
async def get_marketing_data(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: MarketingPortIn = Depends(get_marketing_adapter_in),
    auth_port: JWTAuthPort = Depends(get_jwt_adapter_out)
):
    """
    Endpoint para retornar informações de marketing.
    """
    #await auth_port.validate_token(endpoint_permission="info_production")
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    data = port_in.get_marketing_data(url=url, page=page, page_size=page_size)
    return data