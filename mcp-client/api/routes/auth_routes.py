from fastapi import APIRouter, HTTPException
from utils.google_oauth import get_google_authorization_url, exchange_code_for_tokens
from db.mongodb import create_user, get_user_by_email, verify_password, save_google_tokens
from core.security import generate_access_token
from db.models.users import UserLogin, UserRegister
import jwt

router = APIRouter(
    tags=["auth"]
)

@router.post("/login")
def login(user: UserLogin):
    # Buscar en Mongo
    db_user = get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(user.password, db_user["password"]): 
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Generar el JWT
    user_id = str(db_user["_id"])
    token = generate_access_token(user_id)

    return {
        "success": True,
        "message": "✅ Login exitoso",
        "user_id": user_id,
        "access_token": token
    }

@router.post("/register")
def register(user: UserRegister):
    # Verificar que no exista ya
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    # Crear usuario nuevo
    user_id = create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )

    # Generar el JWT
    token = generate_access_token(user_id)

    return {
        "success": True,
        "message": "✅ Usuario registrado exitosamente",
        "user_id": user_id,
        "access_token": token
    }


@router.get("/google/login")
def google_login():
    """
    Devuelve la URL para redirigir al login de Google
    """
    auth_url = get_google_authorization_url()
    return {"auth_url": auth_url}


@router.get("/google/callback")
def google_callback(code: str):
    """
    Endpoint de redirección de Google con el authorization_code
    """
    try:
        # 1. Intercambiar el code por tokens
        tokens = exchange_code_for_tokens(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exchanging code: {str(e)}")
    
    # 2. Decodificar el ID Token para obtener datos del usuario
    try:
        id_info = jwt.decode(
            tokens["id_token"],
            options={"verify_signature": False, "verify_aud": False},
            algorithms=["RS256"]
        )
        correo = id_info.get("email")
        if not correo:
            raise Exception("No email in ID Token")
        
        given_name = id_info.get("given_name", "")
        family_name = id_info.get("family_name", "")
        name = id_info.get("name", "")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding ID Token: {str(e)}")
    
    # 3. Construir el nombre de usuario a partir de nombre y apellido
    if given_name and family_name:
        usuario = f"{given_name}.{family_name}".replace(" ", "").lower()
    elif name:
        usuario = name.replace(" ", "").lower()
    else:
        usuario = correo.split("@")[0]
    
    # 4. Verificar si el usuario ya existe
    user = get_user_by_email(correo)
    if not user:
        # Crear usuario nuevo
        user = create_user(
            username=usuario,
            email=correo,
            password="" # Puedes dejar vacío o manejar OAuth-only users
        )
    
    token = generate_access_token(user['user_id'])
    # 5. Guardar/actualizar tokens en Mongo
    save_google_tokens(correo, tokens)

    # 6. Responder
    return {
        "success": True,
        "message": f"✅ Login de Google exitoso para {correo}",
        "email": correo,
        "username": usuario,
        "access_token": token,
        "google_tokens": tokens
    }
