from app.domain.models.entities.iam.user import UserEntity
from app.domain.services.iam.db.local_db_service import LocalDbService
from app.domain.exceptions.iam.db.db_exceptions import UserAlreadyExistsError

class SignUpAdapterOut:
    
    def __init__(self, service: LocalDbService):
        self.service = service

    def register_user(self, user: UserEntity):
        """
        Registers a new user in the local database.

        :param user: UserEntity instance containing user data to be registered.
        :return: The registered user data.
        """
        try:
            self.service.register_user(user)
        except UserAlreadyExistsError as e:
            raise UserAlreadyExistsError(f"Error registering user: {str(e)}") from e