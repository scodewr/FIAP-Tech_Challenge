from fastapi import Request, HTTPException, Depends
from app.application.ports.input.iam.auth.jwt_auth_port_in import JWTAuthPortIn
from app.shared.dependencies import get_jwt_adapter_in

def validate_token_and_get_payload(endpoint_permission: str):
    async def dependency(
        request: Request,
        auth_port: JWTAuthPortIn = Depends(get_jwt_adapter_in),
    ):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token ausente ou inválido")

        token = auth.split(" ")[1]
        payload = auth_port.validate_token(token, endpoint_permission)
        return payload

    return Depends(dependency)
