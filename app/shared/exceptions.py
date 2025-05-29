from fastapi import HTTPException, status

class EmbrapaServiceUnavailableException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço Embrapa indisponível. Tente novamente mais tarde."
        )

class EmbrapaDownloadLinkNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Download link não encontrado na página da Embrapa."
        )

class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"}
        )

class ExpiredTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada para acessar este endpoint."
        )