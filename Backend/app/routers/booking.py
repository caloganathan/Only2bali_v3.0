from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import Booking, Trip, get_db
from ..models.schemas import BookingCreate, BookingOut

router = APIRouter()


@router.post(
    "/create-booking",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a booking for a trip",
)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    booking = Booking(
        trip_id=payload.trip_id,
        total_price=payload.total_price,
        status="pending",
        notes=payload.notes,
    )
    db.add(booking)

    trip.status = "booked"

    db.commit()
    db.refresh(booking)

    confirmation_ref = "OB-" + booking.id.replace("-", "")[:8].upper()

    return BookingOut(
        booking_id=booking.id,
        status=booking.status,
        confirmation_ref=confirmation_ref,
        message=f"Your booking is confirmed! Reference: {confirmation_ref}. "
                f"We'll send details to {payload.contact_email}.",
    )
