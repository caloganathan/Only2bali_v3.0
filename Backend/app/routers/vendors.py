from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import VendorOnboarding, get_db
from ..models.schemas import VendorRegisterRequest, VendorRegisterResponse

router = APIRouter()


@router.post(
    "/vendors/register",
    response_model=VendorRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new vendor",
)
def register_vendor(payload: VendorRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(VendorOnboarding).filter(
        VendorOnboarding.email == payload.email,
        VendorOnboarding.category == payload.category.value,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A registration with this email and category already exists.",
        )

    vendor = VendorOnboarding(
        business_name=payload.business_name,
        category=payload.category.value,
        contact_person=payload.contact_person,
        email=payload.email,
        whatsapp=payload.whatsapp,
        location_bali=payload.location_bali,
        price_tier=payload.price_tier.value,
        description=payload.description,
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    return VendorRegisterResponse(
        vendor_id=str(vendor.id),
        status="pending",
        message=(
            "Your vendor registration has been submitted successfully. "
            "Our team will review your application and contact you within 2-3 business days."
        ),
    )


@router.get(
    "/vendors/categories",
    summary="List available vendor categories",
)
def get_categories():
    return {
        "categories": [
            "Indian Food",
            "Transport",
            "Tour Guide",
            "Shopping Souvenirs",
            "Wooden Products",
            "Eatables (Souvenirs)",
            "Batik Products",
        ]
    }
