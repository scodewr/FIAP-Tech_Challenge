from fastapi import APIRouter, Query, Depends, Request
from typing import List
from app.domain.models.entities.embrapa.importation import ImportationEntity
from app.shared.dependencies import get_importation_adapter_in
from app.application.ports.input.embrapa.importation_port_in import ImportationPortIn
from app.shared.util.util_token import validate_token_and_get_payload
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix="/info/importation",
    tags=["Embrapa"],
    dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    summary="Obter dados de importação",
    response_model=List[ImportationEntity],
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
async def get_importation_data(
    request: Request,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ImportationPortIn = Depends(get_importation_adapter_in),
    user_payload: dict = validate_token_and_get_payload(endpoint_permission="info_importation")
):
    """
    Endpoint para retornar informações de importação.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05'
    data = port_in.get_importation_data(url=url, page=page, page_size=page_size)
    return data