from fastapi import APIRouter, Query, Depends
from typing import List
from app.domain.models.entities.embrapa.exportation import ExportationEntity
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from app.shared.dependencies import get_jwt_adapter_out, get_exportation_adapter_in
from app.application.ports.input.embrapa.exportation_port_in import ExportationPortIn

router = APIRouter(
    prefix="/info/exportation",
    tags=["Embrapa"],
    #dependencies=[Depends(HTTPBearer())],
)

@router.get(
    "/",
    summary="Obter dados de exportação",
    response_model=List[ExportationEntity],
    responses={
        200: {
            "description": "Dados de exportação retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "control": "EX",
                            "product": "Vinho",
                            "category": "Exportação",
                            "year": 2020,
                            "exportation": 300
                        },
                        {
                            "id": 2,
                            "control": "EX",
                            "product": "Suco",
                            "category": "Exportação",
                            "year": 2021,
                            "exportation": 400
                        }
                    ]
                }
            },
        },
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
async def get_exportation_data(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    port_in: ExportationPortIn = Depends(get_exportation_adapter_in),
    auth_port: JWTAuthPort = Depends(get_jwt_adapter_out)
):
    """
    Endpoint para retornar informações de exportação.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06'
    data = port_in.get_exportation_data(url=url, page=page, page_size=page_size)
    return data