from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import Trip, User, get_db
from ..models.schemas import TripCreate, TripOut, TripDetail

router = APIRouter()


def compute_lead_score(group_size: int, budget_usd: float = None) -> str:
    if group_size > 4 or (budget_usd is not None and budget_usd > 2000):
        return "high"
    if group_size > 2 or (budget_usd is not None and budget_usd > 1000):
        return "medium"
    return "low"


@router.post(
    "/trips",
    response_model=TripOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new trip",
)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    try:
        date_from = date.fromisoformat(payload.travel_date_from)
        date_to = date.fromisoformat(payload.travel_date_to)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dates must be in YYYY-MM-DD format.",
        )

    if date_to < date_from:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="travel_date_to must be on or after travel_date_from.",
        )

    lead_score = compute_lead_score(payload.group_size, payload.budget_usd)

    trip = Trip(
        user_id=payload.user_id,
        travel_date_from=date_from,
        travel_date_to=date_to,
        group_size=payload.group_size,
        budget_usd=payload.budget_usd,
        status="draft",
        lead_score=lead_score,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    return TripOut(
        trip_id=trip.id,
        status=trip.status,
        lead_score=trip.lead_score,
    )


@router.get(
    "/trips/{trip_id}",
    response_model=TripDetail,
    summary="Get trip details",
)
def get_trip(trip_id: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    return TripDetail(
        trip_id=trip.id,
        user_id=trip.user_id,
        travel_date_from=trip.travel_date_from.isoformat(),
        travel_date_to=trip.travel_date_to.isoformat(),
        group_size=trip.group_size,
        budget_usd=float(trip.budget_usd) if trip.budget_usd is not None else None,
        status=trip.status,
    )
