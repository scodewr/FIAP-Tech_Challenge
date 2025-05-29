from fastapi import APIRouter, Query, Request, Response, Depends
from typing import List
from app.domain.models.entities.exportation import ExportationEntity


router = APIRouter(
    prefix="/info/exportation",
    tags=["Informações de Exportação"],
    
)

@router.get(
    "/",
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
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    """
    Endpoint para retornar informações de exportação.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06'
    return ""