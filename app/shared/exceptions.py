from fastapi import HTTPException, status
from pydantic import ValidationError

class HttpEmbrapaServiceUnavailableException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço Embrapa indisponível. Tente novamente mais tarde."
        )

class HttpEmbrapaDownloadLinkNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Download link não encontrado na página da Embrapa."
        )

class HttpInvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"}
        )

class HttpExpiredTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

class HttpPermissionDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada para acessar este endpoint."
        )

class HttpUserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário já cadastrado."
        )

class HttpPydanticRequestValidationError(HTTPException):
    def __init__(self, error: ValidationError):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.errors() 
        )

class HttpUserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

class HttpInvalidPasswordError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta."
        )