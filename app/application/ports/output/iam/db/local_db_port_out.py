from app.domain.models.entities.iam.user import UserEntity

class LocalDBPortOut:
    """
    Interface for local database output port.
    This interface defines the methods that the local database output port should implement.
    """

    def save_user(self, user):
        """
        Save a user to the local database.
        :param user: The user object to be saved.
        """
        raise NotImplementedError("Method not implemented.")

    def get_user(self, user: UserEntity) -> UserEntity:
        """
        Retrieve a user from the local database by user ID.
        :param user: UserEntity containing user data to be retrieved.
        :return: UserEntity instance containing user data.
        """
        raise NotImplementedError("Method not implemented.")

    def get_user_by_login(self, login: str) -> UserEntity:
        """
        Retrieve a user from the local database by user login.
        :param login: The login of the user to be retrieved.
        :return: UserEntity instance containing user data.
        """
        raise NotImplementedError("Method not implemented.")