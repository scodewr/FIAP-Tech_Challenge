from app.domain.models.entities.iam.user import UserEntity
from app.application.ports.output.iam.auth.permissions_port_out import PermissionsPortOut
from app.shared.dto.iam.user_request_log_in_dto import UserRequestLoginDTO
from app.domain.exceptions.iam.db.db_exceptions import UserAlreadyExistsError
from app.domain.exceptions.iam.model.model_exceptions import PydanticRequestValidationError
from app.application.ports.input.iam.auth.jwt_auth_port_in import JWTAuthPortIn

class LogInService:

    def __init__(self, permissions_port_out: PermissionsPortOut, token_port_in: JWTAuthPortIn):
        """
        Initializes the SignInService with the output port.
        :param permissions_port_out: An instance of LocalDbPortOut to handle user registration.
        :param token_port_in: An instance of JWTAuthPortOut to handle token generation.
        """
        self.permissions_port_out = permissions_port_out
        self.token_port_in = token_port_in
        

    def validate_user_and_get_access_token(self, user_login_dto: UserRequestLoginDTO = None):
        """
        Validates the user data and registers a new user.
        :param user_login_dto: UserRequestDTO containing user data to be registered.
        :raises ValidationError: If the data is invalid.
        """
        if user_login_dto is None:
            raise PydanticRequestValidationError("User data cannot be empty.")
        
        user_data = UserEntity(
            login=user_login_dto.login,
            password=user_login_dto.password,
            first_name="",
            last_name="",
            permissions=[]
        )


        try:
            self.permissions_port_out.validate_user(user_data)
            return self.token_port_in.create_access_token(user_data)
        except UserAlreadyExistsError as e:
            raise UserAlreadyExistsError(f"Error registering user: {str(e)}") from e
        except PydanticRequestValidationError as e:
            raise PydanticRequestValidationError(f"Error validating user data: {str(e)}") from e


