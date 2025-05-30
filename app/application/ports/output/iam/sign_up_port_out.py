from app.domain.models.entities.iam.user import UserEntity

class SignUpPortOut:
    """
    Interface para abstrair os casos de uso relacionados ao cadastro de usuários.
    """

    def register_user(self, user: UserEntity):
        """
        Obtém os dados de produção paginados.

        :param data: Dados do usuário a ser registrado.
        :return: Instância do modelo UserEntity com os dados do usuário.
        """
        raise NotImplementedError("Este método deve ser implementado por um adapter.")
    