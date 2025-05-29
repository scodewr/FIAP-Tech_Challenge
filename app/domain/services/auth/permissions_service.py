from typing import List, Dict
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Dict
import jwt
from fastapi import HTTPException, status
from app.shared.config import settings

class PermissionsService:
    """
    Serviço para validação de permissões e autenticação.
    """
    USERS_DB = {
    "admin": {"password": "password", "permissions": ["info_production", "info_processing", "info_marketing", "info_importation", "info_exportation"]},
    "info_production": {"password": "info_production", "permissions": ["info_production"]},
    "user1": {"password": "user1pass", "permissions": []},  # Sem permissões
}

    def __init__(self):
        self.security = HTTPBearer()  # Classe para autenticação via HTTP Bearer

    def validate_permissions(self, user_permissions: List[str], required_permission: str) -> None:
        """
        Valida se o usuário possui a permissão necessária.

        :param user_permissions: Lista de permissões do usuário.
        :param required_permission: Permissão necessária para acessar o recurso.
        :raises HTTPException: Se o usuário não tiver a permissão necessária.
        """
        if required_permission and required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão negada para acessar este recurso.",
            )

    def validate_token(self, endpoint_permission: str = None):
        """
        Decorator para validação de token JWT e permissões.

        :param endpoint_permission: Permissão necessária para acessar o endpoint.
        :raises HTTPException: Se o token for inválido ou o usuário não tiver permissão.
        """
        def decorator(func):
            async def wrapper(*args, credentials: HTTPAuthorizationCredentials = Depends(self.security), **kwargs):
                token = credentials.credentials
                payload = self.verify_access_token(token)

                # Valida permissões usando o método interno
                self.validate_permissions(payload.get("permissions", []), endpoint_permission)

                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    def verify_access_token(self, token: str) -> Dict:
        """
        Valida o token JWT e retorna os dados decodificados.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    def create_access_token(self, data: Dict) -> str:
        """
        Gera um token JWT com os dados fornecidos.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt