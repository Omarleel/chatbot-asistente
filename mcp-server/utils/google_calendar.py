from datetime import datetime, timedelta

async def find_event_id(service, summary: str, start_time: str, timezone: str = "America/Lima") -> str:
    """
    Busca un evento en el calendario del usuario dado un summary aproximado y start_time.
    Retorna el ID si lo encuentra. Lanza excepción si no hay coincidencia.
    """
    try:
        start_dt = datetime.fromisoformat(start_time)
        time_min = (start_dt - timedelta(hours=1)).isoformat()
        time_max = (start_dt + timedelta(hours=1)).isoformat()

        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            q=summary
        ).execute()

        events = events_result.get('items', [])
        for event in events:
            if summary.lower() in event.get('summary', '').lower():
                return event['id']

        raise ValueError("❌ No se encontró ningún evento que coincida con los criterios.")
    except Exception as e:
        raise ValueError(f"❌ Error al buscar evento: {e}")

