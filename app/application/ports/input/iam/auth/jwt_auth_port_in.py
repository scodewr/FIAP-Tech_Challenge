from typing import Dict
from app.domain.models.entities.iam.user import UserEntity

class JWTAuthPortIn:
    """
    Interface para abstrair as operações relacionadas ao JWT.
    """

    def create_access_token(self, data: UserEntity) -> str:
        """
        Gera um token JWT com os dados fornecidos.

        :param data: Dados a serem incluídos no token.
        :return: Token JWT assinado.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")
    
    def validate_token(self, token: str = None, endpoint_permission: str = None):
        """
        Decorator para validação de token JWT e permissões.

        :param endpoint_permission: Permissão necessária para acessar o endpoint.
        :raises Exception: Se o token for inválido ou o usuário não tiver permissão.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")