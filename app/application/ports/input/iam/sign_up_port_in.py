
from app.shared.dto.iam.user_request_dto import UserRequestDTO
class SignUpPortIn:
    """
    Interface para abstrair os casos de uso relacionados ao cadastro de usuários.
    """

    def new_user(self, user_dto: UserRequestDTO = None):
        """
        Obtém os dados de produção paginados.

        :param user_dto: Dados do usuário a ser registrado.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")