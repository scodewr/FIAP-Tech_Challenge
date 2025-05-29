from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time
from app.shared.config import settings  # Importa as configurações globais

# Configuração do Rate Limiter
rate_limit_data = defaultdict(lambda: {"count": 0, "timestamp": time.time()})

class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar o número de requisições por IP.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        data = rate_limit_data[client_ip]

        # Reseta o contador se o tempo limite foi excedido
        if current_time - data["timestamp"] > 60:
            data["count"] = 0
            data["timestamp"] = current_time

        # Incrementa o contador de requisições
        data["count"] += 1

        # Verifica se o limite foi excedido
        if data["count"] > settings.RATE_LIMIT:  # Usa o RATE_LIMIT definido em settings
            raise HTTPException(
                status_code=429,
                detail="Limite de requisições excedido. Tente novamente mais tarde."
            )

        response = await call_next(request)
        return response

def setup_middleware(app):
    """
    Configura os middlewares na aplicação FastAPI.
    """
    app.add_middleware(RateLimiterMiddleware)