from fastapi import APIRouter, Query, Depends
from typing import List
from app.domain.models.entities.embrapa.importation import ImportationEntity
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from app.shared.dependencies import get_jwt_adapter_out, get_importation_adapter_in
from app.application.ports.input.embrapa.importation_port_in import ImportationPortIn

router = APIRouter(
    prefix="/info/importation",
    tags=["Informações de Importação"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
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
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ImportationPortIn = Depends(get_importation_adapter_in),
    auth_port: JWTAuthPort = Depends(get_jwt_adapter_out)
):
    """
    Endpoint para retornar informações de importação.
    """
    #await auth_port.validate_token(endpoint_permission="info_production")
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05'
    data = port_in.get_importation_data(url=url, page=page, page_size=page_size)
    return data