# Bilal Event Booking System

RESTful service to manage events and book tickets.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Run the Service
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install fastapi uvicorn sqlalchemy`
3. Start the app (within the project root folder):
   - `uvicorn main:app --reload`
4. Open:
   - API: `http://127.0.0.1:8000`
   - Swagger UI: `http://127.0.0.1:8000/docs`

## Database
- The app uses SQLite file: `database.db`
- Tables are created automatically on startup.
- User table is created that contains roles
- roles are :- admin and user, this is done so that certain functionalities can only be performed by admin

## API Endpoints

### User capabilities
- `GET /events/` -> list events
- `POST /bookings` -> book a ticket for an event
- `GET /users/{user_id}/bookings` -> list booked tickets for a user for current and upcoming events

### Owner/admin capabilities
- `POST /events/` -> create event
- `DELETE /events/{event_id}?user_id=<admin_id>` -> delete event
- `GET /events/{event_id}/stats?user_id=<admin_id>` -> get booked ticket count

## Example Requests

### 1) Create an event (admin)
```bash
curl -X POST "http://127.0.0.1:8000/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "name": "Music Night",
    "available_tickets": 100,
    "event_date": "2026-03-20"
  }'
```

### 2) List events
```bash
curl "http://127.0.0.1:8000/events/"
```

### 3) Book a ticket (user)
```bash
curl -X POST "http://127.0.0.1:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "event_id": 1
  }'
```

### 4) List user bookings
```bash
curl "http://127.0.0.1:8000/users/2/bookings"
```

### 5) Event stats (admin)
```bash
curl "http://127.0.0.1:8000/events/1/stats?user_id=1"
```

### 6) Delete event (admin)
```bash
curl -X DELETE "http://127.0.0.1:8000/events/1?user_id=1"
```