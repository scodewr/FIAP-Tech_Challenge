from fastapi import APIRouter, Query, Request, Response, Depends
from typing import List
from app.domain.models.entities.importation import ImportationEntity


router = APIRouter(
    prefix="/info/importation",
    tags=["Informações de Importação"],
    
)

@router.get(
    "/",
    response_model=List[ImportationEntity],
    responses={
        200: {
            "description": "Dados de importação retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "control": "IM",
                            "product": "Vinho",
                            "category": "Importação",
                            "year": 2020,
                            "importation": 150
                        },
                        {
                            "id": 2,
                            "control": "IM",
                            "product": "Suco",
                            "category": "Importação",
                            "year": 2021,
                            "importation": 250
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
async def get_importation_data(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    """
    Endpoint para retornar informações de importação.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05'
    return ""