from fastapi import APIRouter, Depends
from app.application.ports.input.iam.sign_up_port_in import SignUpPortIn
from app.shared.dependencies import get_sign_up_adapter_in
from app.shared.dto.iam.user_request_dto import UserRequestDTO
from app.shared.exceptions import UserAlreadyExistsError, PydanticRequestValidationError
from pydantic import ValidationError

router = APIRouter(
    prefix="/user/sign-up",
    tags=["IAM"],
)


@router.post(
    "/",
    summary="Cadastrar Usuário",
    description="Endpoint para cadastrar um novo usuário no sistema.",
    responses={
        200: {
            "description": "Usuário cadastrado com sucesso.",
            "content": {"application/json": {"example": {"message": "Usuário cadastrado com sucesso."}}},
        },
        409: {
            "description": "Usuário já cadastrado.",
            "content": {"application/json": {"example": {"detail": "Usuário já existe."}}},
        },
    },
)
async def info_production(
    port_in: SignUpPortIn = Depends(get_sign_up_adapter_in),
    user: UserRequestDTO = None
):
    try:
        port_in.new_user(user)
    except Exception as e:
        raise UserAlreadyExistsError() from e
    except ValidationError as e:
        raise PydanticRequestValidationError() from e
    return {"message": "Usuário cadastrado com sucesso."}