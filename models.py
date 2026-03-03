from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    available_tickets = Column(Integer, nullable=False)
    event_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "event_date", name="unique_event_name_date"),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)