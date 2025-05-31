from fastapi import APIRouter, Query, Depends, Request
from typing import List
from app.domain.models.entities.embrapa.processing import ProcessingEntity
from app.application.ports.input.embrapa.processing_port_in import ProcessingPortIn
from fastapi.security import HTTPBearer
from app.shared.util.util_token import validate_token_and_get_payload

from app.shared.dependencies import get_processing_adapter_in

router = APIRouter(
    prefix="/info/processing",
    tags=["Embrapa"],
    dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    summary="Obter dados de processamento",
    response_model=List[ProcessingEntity],
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
async def get_processing_data(
    request: Request,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ProcessingPortIn = Depends(get_processing_adapter_in),
    user_payload: dict = validate_token_and_get_payload(endpoint_permission="info_processing")
):
    """
    Endpoint para retornar informações de processamento.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'
    data = port_in.get_processing_data(url=url, page=page, page_size=page_size)
    return data