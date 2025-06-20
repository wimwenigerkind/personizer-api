# Personizer Python API

A lightweight REST API wrapper for Personizer calendar data, built with FastAPI.

## Overview

This API provides a simple way to access and filter Personizer calendar events through HTTP requests. It fetches iCalendar data from Personizer and allows you to apply various filters to retrieve specific events.

## Authentication

Authentication is handled through the calendar ID or token that is passed directly in the URL path. This token should be kept private as it provides access to your Personizer calendar data.

```
/{cal_id}/events
```

Where `cal_id` is your unique Personizer calendar identifier.

## Endpoints

### GET `/{cal_id}/events`

Retrieves events from a specific Personizer calendar.

#### Path Parameters

- `cal_id` (required): Your Personizer calendar ID or token

#### Query Parameters

- `q` (optional): Filter events by title content (case-insensitive)
- `limit` (optional, default: 10): Maximum number of events to return (1-100)
- `future_only` (optional, default: true): Only include events that haven't started yet
- `days_ahead` (optional): Only include events within the specified number of days (1-365)
- `today` (optional, default: false): Only include events occurring today

#### Response Format

```json
[
  {
    "title": "Event Title",
    "start": "2023-05-15 14:00:00+02:00",
    "end": "2023-05-15 15:00:00+02:00",
    "description": "Event description text",
    "location": "Event location"
  },
  ...
]
```

## Usage Examples

### Get upcoming events

```
GET /{your-calendar-id}/events
```

### Get events for today only

```
GET /{your-calendar-id}/events?today=true
```

### Get events containing "meeting" in the title

```
GET /{your-calendar-id}/events?q=meeting
```

### Get up to 25 events in the next 7 days

```
GET /{your-calendar-id}/events?limit=25&days_ahead=7
```

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   uvicorn main:app --reload
   ```

## Environment Configuration

The API uses the Europe/Berlin timezone by default. You can modify the `TIMEZONE` variable in the code to match your preferred timezone.

## Dependencies

- FastAPI: Web framework
- ics: iCalendar parsing
- requests: HTTP client for fetching calendar data
- python-dateutil: Timezone handling

## License

See the LICENSE file for details.