from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import require_admin_by_user_id, verify_admin
from models import Booking, Event
from schemas import EventCreate, EventResponse, EventStatsResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
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


@router.delete("/{event_id}", dependencies=[Depends(verify_admin)])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # (simple approach) delete related bookings first (SQLite FK behavior can vary)
    db.query(Booking).filter(Booking.event_id == event_id).delete()

    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}


@router.get("/{event_id}/stats", response_model=EventStatsResponse, dependencies=[Depends(verify_admin)])
def event_stats(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    booked = db.query(Booking).filter(Booking.event_id == event_id).count()
    return {"event_id": event_id, "booked_tickets": booked}
