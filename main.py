from fastapi import FastAPI

from Event_booking_API.database import Base, engine
from Event_booking_API.routers import bookings, events

app = FastAPI(title="Bilal Event Booking System")

# Create tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(events.router)
app.include_router(bookings.router)


@app.get("/")
def root():
    return {"message": "Welcome to Bilal event booking system"}