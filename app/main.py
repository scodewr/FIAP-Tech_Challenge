from fastapi import FastAPI
from app.shared.config import settings
from app.shared.middleware import setup_middleware
from app.presentation.production import router as production_router
from app.presentation.processing import router as processing_router
from app.presentation.marketing import router as marketing_router
from app.presentation.importation import router as importation_router
from app.presentation.exportation import router as exportation_router
from app.presentation.sign_up import router as sign_up_router
from app.presentation.log_in import router as log_in_router

# Inicialização do FastAPI
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

# Configuração de middlewares
setup_middleware(app)

# Inclusão dos routers
app.include_router(log_in_router)
app.include_router(sign_up_router)
app.include_router(production_router)
app.include_router(processing_router)
app.include_router(marketing_router)
app.include_router(importation_router)
app.include_router(exportation_router)