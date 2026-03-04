from datetime import date
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    user_id: int
    name: str
    available_tickets: int = Field(gt=0)
    event_date: date


class EventResponse(BaseModel):
    id: int
    name: str
    available_tickets: int
    event_date: date

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: int
    event_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int

    class Config:
        from_attributes = True


class EventStatsResponse(BaseModel):
    event_id: int
    booked_tickets: int


class UserResponse(BaseModel):
    id: int
    role: str
