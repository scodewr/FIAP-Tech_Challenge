from typing import Dict, Callable, Optional
from functools import wraps
import jwt
from app.domain.exceptions.iam.token.token_exceptions import ExpiredTokenException, InvalidTokenException
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException
from app.domain.models.entities.iam.user import UserEntity
from datetime import datetime, timedelta, timezone
from app.shared.config import settings
from app.application.ports.output.iam.auth.permissions_port_out import PermissionsPortOut

class JWTAuthService:

    def __init__(self, permissions_port_out: PermissionsPortOut):
        """
        Initializes the JWTAuthService with the output port.
        :param permissions_port_out: An instance of PermissionsPortOut to handle user permissions.
        """
        self.permissions_port_out = permissions_port_out

    def create_access_token(self, user_data: UserEntity) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        token_data = {
            "sub": user_data.login,
            "permissions": user_data.permissions,
            "exp": expire
        }

        return {'accessToken': jwt.encode(token_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)}

    def validate_token(self, token: str, endpoint_permission: Optional[str] = None):
        """
        Decorator para validar token e permissões.
        
        :param token: JWT extraído do header.
        :param endpoint_permission: Permissão exigida.
        """
        
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            self.permissions_port_out.validate_access_permissions(payload.get("sub"), endpoint_permission)
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException("Token expirado.")
        except jwt.InvalidTokenError:
            raise InvalidTokenException("Token inválido.")
