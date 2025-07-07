import requests
from core.config import settings
from urllib.parse import urlencode

def get_slack_authorization_url() -> str:
    """
    Construye la URL de autorización para Slack OAuth2.
    """
    base_url = "https://slack.com/oauth/v2/authorize"
    params = {
        "client_id": settings.slack_client_id,
        "scope": "chat:write,users:read,channels:read",  # personaliza tus scopes
        "user_scope": "",
        "redirect_uri": settings.slack_redirect_uri
    }
    return f"{base_url}?{urlencode(params)}"


def exchange_code_for_tokens(code: str) -> dict:
    """
    Intercambia el code de autorización por tokens de Slack.
    """
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "client_id": settings.slack_client_id,
        "client_secret": settings.slack_client_secret,
        "code": code,
        "redirect_uri": settings.slack_redirect_uri
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        raise Exception(f"Slack OAuth Error: {result}")

    return {
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),  # Slack only returns if enabled for app
        "scope": result.get("scope"),
        "bot_user_id": result.get("bot_user_id"),
        "team": result.get("team", {}),
        "authed_user": result.get("authed_user", {})
    }


def refresh_credentials(refresh_token: str) -> dict:
    """
    Usa un refresh_token para obtener un nuevo access_token en Slack.
    Solo funciona si tu app tiene refresh tokens habilitados.
    """
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.slack_client_id,
        "client_secret": settings.slack_client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        raise Exception(f"Slack refresh error: {result}")

    return {
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),
        "scope": result.get("scope"),
        "bot_user_id": result.get("bot_user_id"),
        "team": result.get("team", {}),
        "authed_user": result.get("authed_user", {})
    }


def is_slack_token_valid(access_token: str) -> bool:
    """
    Verifica si un token de Slack es válido.
    """
    try:
        response = requests.post(
            "https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5
        )
        result = response.json()
        return result.get("ok", False)
    except requests.RequestException:
        return False
