from fastapi import APIRouter, Query, Depends
from typing import List
from app.domain.models.entities.embrapa.marketing import MarketingEntity
from fastapi.security import HTTPBearer
from app.application.ports.input.embrapa.marketing_port_in import MarketingPortIn

from app.shared.dependencies import get_marketing_adapter_in

router = APIRouter(
    prefix="/info/marketing",
    tags=["Embrapa"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    summary="Obter dados de marketing",
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
    port_in: MarketingPortIn = Depends(get_marketing_adapter_in)
):
    """
    Endpoint para retornar informações de marketing.
    """
    #await auth_port.validate_token(endpoint_permission="info_production")
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    data = port_in.get_marketing_data(url=url, page=page, page_size=page_size)
    return data