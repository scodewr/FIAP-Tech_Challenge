from app.domain.models.entities.iam.user import UserEntity
from app.domain.exceptions.iam.db.db_exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidPasswordError

class LocalDbService:
    """
    LocalDbService is a service that provides an interface for interacting with a local database.
    It is used to manage user data and other related operations.
    """

    db = {
        "users": {
            "admin": UserEntity(
                id=1,
                login="admin",
                first_name="Admin",
                last_name="Service User",
                password="admin123",
                permissions=["info_production", "info_processing", "info_marketing", "info_importation", "info_exportation"]
            )
        }
}



    def register_user(self, user: UserEntity):
        """
        Registers a new user in the local database.
        
        :param user: User data to be registered.
        :return: The registered user data.
        """

        login = user.login

        if login in self.db["users"]:
            raise UserAlreadyExistsError(f"Usuário '{login}' já existe.")
        
        user.id = len(self.db["users"]) + 1
        self.db["users"][login] = user


    def get_user(self, user: UserEntity) -> UserEntity:
        """
        Retrieves a user from the local database by login.
        
        :param user: User data containing the login to be retrieved.
        :return: The user data if found, None otherwise.
        """
        try:
            user_entity = self.db["users"][user.login]
            if user is None:
                raise UserNotFoundError(f"User '{user.login}' not found.")
            if user.password != user_entity.password:
                raise InvalidPasswordError(f"Invalid password for user '{user.login}'.")
            return user_entity
        except UserNotFoundError as e:
            raise UserNotFoundError(f"User '{user.login}' not found.") from e
        except InvalidPasswordError as e:
            raise InvalidPasswordError(f"Invalid password for user '{user.login}'.") from e
        
    def get_user_by_login(self, login: str) -> UserEntity:
        """
        Retrieves a user from the local database by login.
        
        :param login: The login of the user to be retrieved.
        :return: The user data if found, None otherwise.
        """
        if login in self.db["users"]:
            return self.db["users"][login]
        else:
            raise UserNotFoundError(f"User with login '{login}' not found.")

    def delete_user(self, user_id):
        raise NotImplementedError("Delete user operation is not implemented in LocalDbService.")