import json
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import Itinerary, Trip, get_db
from ..models.schemas import ItineraryRequest, ItineraryOut
from ..services.ai_engine import generate_itinerary, _fallback_itinerary

router = APIRouter()


@router.post(
    "/generate-itinerary",
    response_model=ItineraryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Generate an AI itinerary for a trip",
)
def create_itinerary(payload: ItineraryRequest, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    days = generate_itinerary(
        user_prefs=payload.user_prefs,
        dates=payload.dates,
        group_size=payload.group_size,
        budget_usd=payload.budget_usd,
    )

    if not days:
        days = _fallback_itinerary(payload.dates)

    itinerary_group_id = str(uuid.uuid4())

    saved_rows = []
    for day_obj in days:
        day_number = day_obj.get("day", len(saved_rows) + 1)
        row = Itinerary(
            id=str(uuid.uuid4()),
            trip_id=payload.trip_id,
            day_number=day_number,
            plan=json.dumps(day_obj),
            ai_generated=True,
        )
        db.add(row)
        saved_rows.append(row)

    db.commit()

    total_cost = sum(
        float(d.get("estimated_cost_usd", 0)) for d in days
    )

    return ItineraryOut(
        itinerary_id=itinerary_group_id,
        trip_id=payload.trip_id,
        days=days,
        total_estimated_cost_usd=total_cost,
    )
