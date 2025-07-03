import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
from core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]
CLIENT_SECRET_FILE = settings.google_client_secret


def run_local_server_flow() -> str:
    """
    Lanza el navegador local para logueo y devuelve tokens en JSON (texto).
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES
    )

    creds = flow.run_local_server(port=0)

    # Armamos respuesta JSON
    data = {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "id_token": creds.id_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }
    return json.dumps(data, indent=2)


def is_google_token_valid(access_token: str) -> bool:
    """
    Verifica si un access_token es válido llamando al endpoint de userinfo.
    """
    try:
        response = requests.get(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=5
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def refresh_credentials(refresh_token: str) -> str:
    """
    Usa un refresh_token para obtener un nuevo access_token.
    Retorna JSON (texto) con los nuevos datos.
    """
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret_value,
        scopes=SCOPES
    )
    creds.refresh(Request())

    data = {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "id_token": creds.id_token,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }
    return json.dumps(data, indent=2)
