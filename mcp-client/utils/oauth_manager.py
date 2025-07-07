from typing import Dict, Any, Optional
from db.mongodb import (
    get_google_tokens_by_user_id,
    save_google_tokens_by_id,
    get_slack_tokens_by_user_id,
    save_slack_tokens_by_id
)
from utils.google_oauth import (
    is_google_token_valid,
    get_google_authorization_url,
    refresh_credentials as google_refresh
)
from utils.slack_oauth import (
    is_slack_token_valid,
    get_slack_authorization_url,
    refresh_credentials as slack_refresh
)

def handle_provider_oauth(
    provider_name: str,
    user_id: str
) -> Dict[str, Any]:
    """
    Manejador genérico para un proveedor.
    """
    valid_token = None
    reauth_url = None

    if provider_name == "google":
        tokens = get_google_tokens_by_user_id(user_id)
        if not tokens or not isinstance(tokens, dict) or 'access_token' not in tokens:
            return {"valid_token": None, "reauth_url": get_google_authorization_url()}

        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        if not is_google_token_valid(access_token):
            if refresh_token:
                try:
                    refreshed = google_refresh(refresh_token)
                    access_token = refreshed['access_token']
                    tokens.update(refreshed)
                    save_google_tokens_by_id(user_id, tokens)
                except Exception:
                    access_token = None
                    reauth_url = get_google_authorization_url()
            else:
                reauth_url = get_google_authorization_url()

        if not access_token:
            reauth_url = get_google_authorization_url()

        return {"valid_token": access_token, "reauth_url": reauth_url}

    elif provider_name == "slack":
        tokens = get_slack_tokens_by_user_id(user_id)
        if not tokens or not isinstance(tokens, dict) or 'access_token' not in tokens:
            return {"valid_token": None, "reauth_url": get_slack_authorization_url()}

        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        if not is_slack_token_valid(access_token):
            if refresh_token:
                try:
                    refreshed = slack_refresh(refresh_token)
                    access_token = refreshed['access_token']
                    tokens.update(refreshed)
                    save_slack_tokens_by_id(user_id, tokens)
                except Exception:
                    access_token = None
                    reauth_url = get_slack_authorization_url()
            else:
                reauth_url = get_slack_authorization_url()

        if not access_token:
            reauth_url = get_slack_authorization_url()

        return {"valid_token": access_token, "reauth_url": reauth_url}

    else:
        return {"valid_token": None, "reauth_url": None}


def manage_all_oauth(user_id: str) -> Dict[str, Any]:
    """
    Maneja todos los providers soportados y devuelve tokens y URLs de reautorización.
    """
    providers = ["google", "slack"]  # Extiende aquí si agregas más
    valid_tokens = {}
    reauthorize_urls = {}

    for provider in providers:
        result = handle_provider_oauth(provider, user_id)
        if result.get("valid_token"):
            valid_tokens[provider] = result["valid_token"]
        if result.get("reauth_url"):
            reauthorize_urls[provider] = result["reauth_url"]

    return {
        "valid_tokens": valid_tokens,
        "reauthorize_urls": reauthorize_urls
    }
