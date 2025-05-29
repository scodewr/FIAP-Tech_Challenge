from fastapi import APIRouter, Query, Request, Response, Depends
from typing import List
from app.domain.models.entities.processing import ProcessingEntity



router = APIRouter(
    prefix="/info/processing",
    tags=["Informações de Processamento"],
    
)

@router.get(
    "/",
    response_model=List[ProcessingEntity],
    responses={
        200: {
            "description": "Dados de processamento retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "control": "PR",
                            "cultivate": "Uva",
                            "category": "Processamento",
                            "year": 2020,
                            "processing": 300
                        },
                        {
                            "id": 2,
                            "control": "AR",
                            "cultivate": "Uva",
                            "category": "Armazenamento",
                            "year": 2021,
                            "processing": 400
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
async def get_processing_data(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    """
    Endpoint para retornar informações de processamento.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'
    data = processing_adapter.get_production_data(url=url, page=page, page_size=page_size)
    return data