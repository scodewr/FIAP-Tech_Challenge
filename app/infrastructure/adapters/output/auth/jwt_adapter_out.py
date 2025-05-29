from typing import Dict
from app.application.ports.output.auth.jwt_auth_port import JWTAuthPort
from app.domain.services.auth.permissions_service import PermissionsService

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta_super_segura"  # Substitua por uma chave secreta forte
ALGORITHM = "HS256"  # Algoritmo de assinatura
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token (em minutos)

class JWTAdapterOut(JWTAuthPort):
    """
    Adapter para interagir com a biblioteca JWT.
    """

    def __init__(self, permissions_service: PermissionsService):
        self.permissions_service = permissions_service

    def create_access_token(self, data: Dict) -> str:
        """
        Gera um token JWT com os dados fornecidos.
        """
        return self.permissions_service.create_access_token(data)

    def validate_token(self, endpoint_permission: str = None):
        """
        Decorator para validação de token JWT e permissões.
        """
        return self.permissions_service.validate_token(endpoint_permission)