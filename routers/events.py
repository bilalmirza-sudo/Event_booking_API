from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import require_admin_by_user_id
from models import Booking, Event
from schemas import EventCreate, EventResponse, EventStatsResponse

router = APIRouter(prefix="/events", tags=["events"])

# A user can see list of all of the events happening in the present and future
@router.get("/", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    # TODO: Add pagination (e.g., limit/offset) for scalability.
    events = (
        db.query(Event)
        .filter(Event.available_tickets > 0, Event.event_date >= date.today())
        .all()
    )
    if not events:
        raise HTTPException(status_code=404, detail="No available events")
    return events

# A particular event details can be fetched
@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Create an event 
# A user with role "admin" can perform this action
@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    if event.event_date < date.today():
        raise HTTPException(status_code=400, detail="Please  select  correct date")

    require_admin_by_user_id(user_id=event.user_id, db=db)

    existing = (
        db.query(Event)
        .filter(Event.name == event.name, Event.event_date == event.event_date)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Event already exists")

    new_event = Event(
        name=event.name,
        available_tickets=event.available_tickets,
        event_date=event.event_date,
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# Delete an event
# Here the event is manually deleted by the admin
@router.delete("/{event_id}")
def delete_event(event_id: int, user_id: int, db: Session = Depends(get_db)):
    require_admin_by_user_id(user_id=user_id, db=db)

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # (simple approach) delete related bookings first (SQLite FK behavior can vary)
    db.query(Booking).filter(Booking.event_id == event_id).delete()

    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}

# Admin can see events statistics
@router.get("/{event_id}/stats", response_model=EventStatsResponse)
def event_stats(event_id: int, user_id: int, db: Session = Depends(get_db)):
    require_admin_by_user_id(user_id=user_id, db=db)

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    booked = db.query(Booking).filter(Booking.event_id == event_id).count()
    return {"event_id": event_id, "booked_tickets": booked}
