from app.application.ports.input.iam.log_in_port_in import LogInPortIn
from app.shared.dto.iam.user_request_log_in_dto import UserRequestLoginDTO
from app.domain.services.iam.log_in_service import LogInService
from app.domain.exceptions.iam.db.db_exceptions import UserNotFoundError, InvalidPasswordError
from app.domain.exceptions.iam.token.token_exceptions import ExpiredTokenException, InvalidTokenException
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException

class LogInAdapterIn(LogInPortIn):
    def __init__(self, service: LogInService):
        self.service = service

    def log_in(self, user_login_dto: UserRequestLoginDTO = None) -> str:
        try:
            return self.service.validate_user_and_get_access_token(user_login_dto=user_login_dto)
        except UserNotFoundError as e:
            raise UserNotFoundError() from e
        except InvalidPasswordError as e:
            raise InvalidPasswordError() from e
        except PermissionDeniedException as e:
            raise PermissionDeniedException() from e
        except ExpiredTokenException as e:
            raise ExpiredTokenException() from e
        except InvalidTokenException as e:
            raise InvalidTokenException() from e