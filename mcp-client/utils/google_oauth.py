import json
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from core.config import settings
import requests

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def build_flow():
    return Flow.from_client_secrets_file(
        settings.google_client_secret,
        scopes=SCOPES,
        redirect_uri=settings.google_redirect_uri
    )

def get_google_authorization_url():
    flow = build_flow()
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline',
        include_granted_scopes='true'
    )
    return auth_url

def exchange_code_for_tokens(code: str):
    flow = build_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials
    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "id_token": creds.id_token,
        "expiry": creds.expiry.isoformat() if creds.expiry else None
    }

def is_google_token_valid(token: str) -> bool:
    """
    Verifica si un token de Google es válido.
    Hace una llamada a la endpoint de Userinfo (OpenID Connect).
    Devuelve True si es válido, False si no.
    """
    try:
        response = requests.get(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'Bearer {token}'},
            timeout=5
        )
        if response.status_code == 200:
            return True
        else:
            return False
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
