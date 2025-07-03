import requests

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

