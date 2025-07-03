from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests
from utils.google_auth import is_google_token_valid
from models.google_calendar_response import CalendarResponse
import logging

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def get_calendar_service_from_token(access_token: str):
    creds = Credentials(token=access_token, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def register(mcp):
    @mcp.tool()
    async def create_event(access_token: str, summary: str, start_time: str, duration_minutes: int = 60, timezone: str = "America/Lima") -> CalendarResponse:
        try:
            # ✅ Primero validamos el token
            if not is_google_token_valid(access_token):
                return CalendarResponse(
                    success=False,
                    message="❌ Token inválido o expirado. Por favor vuelve a autenticarte."
                )

            # ✅ Creamos el servicio con el token
            service = get_calendar_service_from_token(access_token)
    
            # ✅ Parseamos las fechas
            start_dt = datetime.fromisoformat(start_time)
            end_dt = start_dt + timedelta(minutes=duration_minutes)

            # ✅ Definimos el evento
            event = {
                'summary': summary,
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': timezone},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': timezone}
            }

            # ✅ Insertamos el evento en el calendario
            created = service.events().insert(calendarId='primary', body=event).execute()
            userinfo = requests.get(
                'https://openidconnect.googleapis.com/v1/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            ).json()
            return CalendarResponse(
                success=True,
                message=f'✅ Evento creado exitosamente para {userinfo["email"]}.',
                url=created.get('htmlLink')
            )

        except Exception as e:
            logger.error(f"❌ Error al crear evento: {e}", exc_info=True)
            return CalendarResponse(
                success=False,
                message=f"❌ Error al crear evento: {e}"
            )
