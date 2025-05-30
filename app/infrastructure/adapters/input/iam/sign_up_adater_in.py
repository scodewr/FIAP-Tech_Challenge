from pydantic import ValidationError
from app.application.ports.input.iam.sign_up_port_in import SignUpPortIn
from app.shared.dto.iam.user_request_dto import UserRequestDTO
from app.domain.services.iam.sign_up_service import SignUpService

class SignUpAdapterIn(SignUpPortIn):
    def __init__(self, service: SignUpService):
        self.service = service

    def new_user(self, user_dto: UserRequestDTO = None):
        try:
            self.service.validate_and_register_user(user_dto=user_dto)
        except ValidationError as e:
            raise Exception(f"Erro ao cadastrar usuário: {str(e)}") from e