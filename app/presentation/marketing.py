from fastapi import APIRouter, Query, Request, Response, Depends
from typing import List
from app.domain.models.entities.marketing import MarketingEntity


router = APIRouter(
    prefix="/info/marketing",
    tags=["Informações de Marketing"],
    
)

@router.get(
    "/",
    response_model=List[MarketingEntity],
    responses={
        200: {
            "description": "Dados de marketing retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "control": "MK",
                            "campaign": "Campanha de Marketing",
                            "category": "Marketing",
                            "year": 2020,
                            "marketing": 500
                        },
                        {
                            "id": 2,
                            "control": "AD",
                            "campaign": "Publicidade",
                            "category": "Publicidade",
                            "year": 2021,
                            "marketing": 300
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
async def get_marketing_data(
    request: Request,
    response: Response,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    """
    Endpoint para retornar informações de marketing.
    """
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    return ""