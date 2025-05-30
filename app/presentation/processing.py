from fastapi import APIRouter, Query, Depends
from typing import List
from app.domain.models.entities.embrapa.processing import ProcessingEntity
from app.application.ports.input.embrapa.processing_port_in import ProcessingPortIn
from fastapi.security import HTTPBearer
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from app.shared.dependencies import get_jwt_adapter_out, get_processing_adapter_in

router = APIRouter(
    prefix="/info/processing",
    tags=["Informações de Processamento"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
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
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ProcessingPortIn = Depends(get_processing_adapter_in),
    auth_port: JWTAuthPort = Depends(get_jwt_adapter_out)
):
    """
    Endpoint para retornar informações de processamento.
    """
    #await auth_port.validate_token(endpoint_permission="info_production")
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'
    data = port_in.get_processing_data(url=url, page=page, page_size=page_size)
    return data