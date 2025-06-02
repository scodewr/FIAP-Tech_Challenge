from fastapi import Request, HTTPException, Depends
from app.application.ports.input.iam.auth.jwt_auth_port_in import JWTAuthPortIn
from app.shared.dependencies import get_jwt_adapter_in
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException
from app.domain.exceptions.iam.db.db_exceptions import UserNotFoundError
from app.domain.exceptions.iam.token.token_exceptions import ExpiredTokenException, InvalidTokenException
from app.shared.exceptions import HttpPermissionDeniedException, HttpUserNotFoundError, HttpExpiredTokenException, HttpInvalidTokenException

def validate_token_and_get_payload(endpoint_permission: str):
    async def dependency(
        request: Request,
        auth_port: JWTAuthPortIn = Depends(get_jwt_adapter_in),
    ):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token ausente ou inválido")

        token = auth.split(" ")[1]
        try: 
            payload = auth_port.validate_token(token, endpoint_permission)
            return payload
        except PermissionDeniedException as e:
            raise HttpPermissionDeniedException() from e
        except UserNotFoundError as e:
            raise HttpUserNotFoundError() from e
        except InvalidTokenException as e:
            raise HttpInvalidTokenException() from e
        except ExpiredTokenException as e:
            raise HttpExpiredTokenException() from e

    return Depends(dependency)
