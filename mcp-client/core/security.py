import jwt
from pathlib import Path
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ✅ Claves RSA en PEM
PRIVATE_KEY = Path("private_key.pem").read_text()
PUBLIC_KEY = Path("public_key.pem").read_text()

ISSUER = "https://example.com"
AUDIENCE = "mi-mcp-server"

# ✅ FastAPI security scheme
auth_scheme = HTTPBearer()

# ✅ Generar token firmado
def generate_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=3)
    payload = {
        "sub": user_id,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "exp": expire
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token


# ✅ Decodificar y verificar token
def decode_access_token(token: str) -> dict:
    """
    Verifica la firma del token con la public_key.
    Devuelve el payload decodificado si es válido.
    Lanza jwt.exceptions si es inválido o expirado.
    """
    return jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=["RS256"],
        issuer=ISSUER,
        audience=AUDIENCE
    )


# ✅ Dependency para FastAPI
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    token = credentials.credentials

    # Validación básica de formato JWT
    if not token or token.count('.') != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ Token mal formado: se esperaba formato JWT (header.payload.signature)"
        )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="❌ Token válido pero sin claim 'sub'"
            )
        return {
            'user_id': user_id,
            'token': token
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ Token expirado."
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"❌ Token inválido: {e}"
        )