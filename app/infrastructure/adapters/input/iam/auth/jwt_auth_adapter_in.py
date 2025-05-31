from typing import Dict
from app.application.ports.input.iam.auth.jwt_auth_port_in import JWTAuthPortIn
from app.domain.services.iam.auth.jwt_auth_service import JWTAuthService
from app.domain.models.entities.iam.user import UserEntity

class JWTAuthAdapterIn(JWTAuthPortIn):
    """
    Adapter para interagir com a biblioteca JWT.
    """

    def __init__(self, service: JWTAuthService):
        self.service = service

    def create_access_token(self, user: UserEntity) -> str:
        """
        Gera um token JWT com os dados fornecidos.
        """
        return self.service.create_access_token(user)

    def validate_token(self, token: str = None, endpoint_permission: str = None):
        """
        Decorator para validação de token JWT e permissões.
        """
        return self.service.validate_token(token, endpoint_permission)