from fastapi import APIRouter, Depends
from app.application.ports.input.iam.log_in_port_in import LogInPortIn
from app.shared.dependencies import get_log_in_adapter_in
from app.shared.dto.iam.user_request_log_in_dto import UserRequestLoginDTO
from app.shared.exceptions import HttpExpiredTokenException, HttpInvalidTokenException, HttpPermissionDeniedException, HttpInvalidPasswordError, HttpUserNotFoundError
from app.domain.exceptions.iam.db.db_exceptions import UserNotFoundError, InvalidPasswordError
from app.domain.exceptions.iam.token.token_exceptions import ExpiredTokenException, InvalidTokenException
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException

router = APIRouter(
    prefix="/user/log-in",
    tags=["IAM"],
)


@router.post(
    "/",
    summary="Logar Usuário",
    description="Endpoint para logar com usuário válido e obter token para acessar recursos no sistema.",
    responses={
        200: {
            "access_token": "Bearer <token>",
            "content": {"application/json": {"example": {"message": "Usuário logado com sucesso."}}},
        },
        404: {
            "description": "Usuário não encontrado.",
            "content": {"application/json": {"example": {"detail": "Usuário não encontrado."}}},
        },
        401: {
            "description": "Senha inválida.",
            "content": {"application/json": {"example": {"detail": "Senha inválida."}}},
        },
        403: {
            "description": "Permissão negada.",
            "content": {"application/json": {"example": {"detail": "Permissão negada."}}},
        },
    },
)
async def info_production(
    port_in: LogInPortIn = Depends(get_log_in_adapter_in),
    user: UserRequestLoginDTO = None
):
    try:
        return port_in.log_in(user)
    except UserNotFoundError as e:
        raise HttpUserNotFoundError() from e
    except InvalidPasswordError as e:
        raise HttpInvalidPasswordError() from e
    except PermissionDeniedException as e:
        raise HttpPermissionDeniedException() from e
    except ExpiredTokenException as e:
        raise HttpExpiredTokenException() from e
    except InvalidTokenException as e:
        raise HttpInvalidTokenException() from e