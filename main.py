from fastapi import FastAPI, Query, Path
from ics import Calendar
import requests
from datetime import datetime, timedelta
from dateutil import tz

app = FastAPI()

ICS_URL = "https://www.personizer.com/ical/"
TIMEZONE = tz.gettz("Europe/Berlin")

def fetch_events(cal_id: str):
    ics_data = requests.get(ICS_URL + cal_id).text
    calendar = Calendar(ics_data)
    return sorted(calendar.events, key=lambda e: e.begin)

@app.get("/{cal_id}/events")
def get_events(
    cal_id: str = Path(..., description="Kalender-ID oder Token"),
    q: str = Query(None, description="Filter nach Titelinhalt"),
    limit: int = Query(10, ge=1, le=100),
    future_only: bool = Query(True),
    days_ahead: int = Query(None, ge=1, le=365),
    today: bool = Query(False, description="Nur Events vom heutigen Tag"),
):
    now = datetime.now(tz=TIMEZONE)
    events = fetch_events(cal_id)

    result = []

    for event in events:
        start = event.begin.datetime.astimezone(TIMEZONE)

        if today:
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            if not (today_start <= start < today_end):
                continue

        elif future_only and start < now:
            continue

        elif days_ahead:
            end_date = now + timedelta(days=days_ahead)
            if start > end_date:
                continue

        if q and q.lower() not in event.name.lower():
            continue

        result.append({
            "title": event.name,
            "start": str(event.begin),
            "end": str(event.end),
            "description": event.description,
            "location": event.location,
        })

        if len(result) >= limit:
            break

    return result
