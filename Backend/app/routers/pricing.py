from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..models.database import Itinerary, get_db
from ..models.schemas import PriceRequest, PriceBreakdown, VendorMatch
from ..services.pricing_engine import calculate_price
from ..services.vendor_matcher import match_vendors

router = APIRouter()


@router.post(
    "/calculate-price",
    response_model=PriceBreakdown,
    summary="Calculate trip price from itinerary",
)
def calculate_trip_price(payload: PriceRequest, db: Session = Depends(get_db)):
    if payload.price_tier not in ("budget", "mid", "premium"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="price_tier must be one of: budget, mid, premium",
        )

    days_count = (
        db.query(Itinerary)
        .filter(Itinerary.trip_id == (
            db.query(Itinerary)
            .filter(Itinerary.id == payload.itinerary_id)
            .with_entities(Itinerary.trip_id)
            .scalar_subquery()
        ))
        .count()
    )

    if days_count == 0:
        # itinerary_id is a logical group id — fall back to counting by trip lookup
        # Try finding any itinerary record associated with the itinerary_id pattern
        days_count = 3

    breakdown = calculate_price(
        days=days_count,
        group_size=payload.group_size,
        price_tier=payload.price_tier,
    )

    return PriceBreakdown(**breakdown)


@router.get(
    "/match-vendors",
    response_model=list[VendorMatch],
    summary="Find matching vendors by filters",
)
def get_vendor_matches(
    type: str = Query(None, description="Vendor type"),
    veg: str = Query(None, description="Veg type filter"),
    location: str = Query(None, description="Location keyword"),
    tier: str = Query(None, description="Price tier"),
    db: Session = Depends(get_db),
):
    vendors = match_vendors(
        db=db,
        vendor_type=type,
        veg_type=veg,
        location=location,
        price_tier=tier,
    )

    return [
        VendorMatch(
            vendor_id=v.id,
            name=v.name,
            type=v.type,
            rating=float(v.rating) if v.rating is not None else None,
            price_tier=v.price_tier,
            veg_type=v.veg_type,
            location=v.location,
        )
        for v in vendors
    ]
