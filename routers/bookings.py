from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Booking, Event
from ..schemas import BookingCreate, BookingResponse

router = APIRouter(tags=["bookings"])


@router.post("/bookings", response_model=BookingResponse)
def book_ticket(payload: BookingCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == payload.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.available_tickets <= 0:
        raise HTTPException(status_code=409, detail="No tickets available")

    booking = Booking(user_id=payload.user_id, event_id=payload.event_id)

    # create booking + decrement tickets
    db.add(booking)
    event.available_tickets -= 1
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/users/{user_id}/bookings", response_model=list[BookingResponse])
def list_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == user_id).all()