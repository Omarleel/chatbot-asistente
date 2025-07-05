from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests
from utils.google_auth import is_google_token_valid
from models.google_calendar_response import CalendarResponse
import logging
from utils.google_calendar import find_event_id
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
        
    @mcp.tool()
    async def get_event(access_token: str, summary: str, start_time: str, timezone: str = "America/Lima") -> CalendarResponse:
        try:
            if not is_google_token_valid(access_token):
                return CalendarResponse(success=False, message="❌ Token inválido o expirado.")

            service = get_calendar_service_from_token(access_token)
            event_id = await find_event_id(service, summary, start_time, timezone)

            event = service.events().get(calendarId='primary', eventId=event_id).execute()

            return CalendarResponse(
                success=True,
                message=f"✅ Evento encontrado: {event.get('summary')}",
                url=event.get('htmlLink')
            )
        except Exception as e:
            logger.error(f"❌ Error al obtener evento: {e}", exc_info=True)
            return CalendarResponse(success=False, message=f"❌ Error al obtener evento: {e}")

    @mcp.tool()
    async def update_event(access_token: str, summary: str, start_time: str, new_summary: str = None, new_start_time: str = None, new_duration_minutes: int = None, timezone: str = "America/Lima") -> CalendarResponse:
        try:
            if not is_google_token_valid(access_token):
                return CalendarResponse(success=False, message="❌ Token inválido o expirado.")

            service = get_calendar_service_from_token(access_token)
            event_id = await find_event_id(service, summary, start_time, timezone)

            event = service.events().get(calendarId='primary', eventId=event_id).execute()

            if new_summary:
                event['summary'] = new_summary
            if new_start_time and new_duration_minutes:
                new_start_dt = datetime.fromisoformat(new_start_time)
                new_end_dt = new_start_dt + timedelta(minutes=new_duration_minutes)
                event['start'] = {'dateTime': new_start_dt.isoformat(), 'timeZone': timezone}
                event['end'] = {'dateTime': new_end_dt.isoformat(), 'timeZone': timezone}

            updated = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()

            return CalendarResponse(
                success=True,
                message=f"✅ Evento actualizado: {updated.get('summary')}",
                url=updated.get('htmlLink')
            )
        except Exception as e:
            logger.error(f"❌ Error al actualizar evento: {e}", exc_info=True)
            return CalendarResponse(success=False, message=f"❌ Error al actualizar evento: {e}")

    @mcp.tool()
    async def delete_event(access_token: str, summary: str, start_time: str, timezone: str = "America/Lima") -> CalendarResponse:
        try:
            if not is_google_token_valid(access_token):
                return CalendarResponse(success=False, message="❌ Token inválido o expirado.")

            service = get_calendar_service_from_token(access_token)
            event_id = await find_event_id(service, summary, start_time, timezone)

            service.events().delete(calendarId='primary', eventId=event_id).execute()

            return CalendarResponse(
                success=True,
                message=f"✅ Evento eliminado correctamente.",
                url=None
            )
        except Exception as e:
            logger.error(f"❌ Error al eliminar evento: {e}", exc_info=True)
            return CalendarResponse(success=False, message=f"❌ Error al eliminar evento: {e}")
