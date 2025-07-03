from google_auth_oauthlib.flow import Flow
from core.config import settings

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
