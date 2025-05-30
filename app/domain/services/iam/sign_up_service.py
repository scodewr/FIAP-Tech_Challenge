from app.domain.models.entities.iam.user import UserEntity
from app.application.ports.output.iam.sign_up_port_out import SignUpPortOut
from app.shared.dto.iam.user_request_dto import UserRequestDTO
from app.domain.exceptions.iam.db.general_exceptions import UserAlreadyExistsError

class SignUpService:

    def __init__(self, port_out: SignUpPortOut):
        """
        Initializes the SignInService with the output port.
        :param port_out: An instance of SingInPortOut to handle user registration.
        """
        self.port_out = port_out
        

    def validate_and_register_user(self, user_dto: UserRequestDTO = None):
        """
        Validates the user data and registers a new user.
        :param user_dto: UserRequestDTO containing user data to be registered.
        :raises ValidationError: If the data is invalid.
        """
        if user_dto is None:
            raise ValueError("User data cannot be empty.")
        user = user_dto.model_dump_json()
        user_data = UserEntity.model_validate_json(user)

        try:
            self.port_out.register_user(user_data)
        except UserAlreadyExistsError as e:
            raise UserAlreadyExistsError(f"Error registering user: {str(e)}") from e
        


