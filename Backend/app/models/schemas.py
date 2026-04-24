from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class VendorCategory(str, Enum):
    INDIAN_FOOD = "Indian Food"
    TRANSPORT = "Transport"
    TOUR_GUIDE = "Tour Guide"
    SHOPPING_SOUVENIRS = "Shopping Souvenirs"
    WOODEN_PRODUCTS = "Wooden Products"
    EATABLES_SOUVENIRS = "Eatables (Souvenirs)"
    BATIK_PRODUCTS = "Batik Products"


class PriceTier(str, Enum):
    BUDGET = "budget"
    MID = "mid"
    PREMIUM = "premium"


class VendorRegisterRequest(BaseModel):
    business_name: str
    category: VendorCategory
    contact_person: str
    email: EmailStr
    whatsapp: str
    location_bali: str
    price_tier: PriceTier
    description: Optional[str] = None

    @field_validator("business_name", "contact_person", "whatsapp", "location_bali")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("whatsapp")
    @classmethod
    def valid_whatsapp(cls, v: str) -> str:
        digits = v.replace("+", "").replace("-", "").replace(" ", "")
        if not digits.isdigit() or len(digits) < 8:
            raise ValueError("Enter a valid WhatsApp number")
        return v.strip()


class VendorRegisterResponse(BaseModel):
    vendor_id: str
    status: str
    message: str


class VendorListItem(BaseModel):
    vendor_id: str
    business_name: str
    category: str
    location_bali: str
    price_tier: str
    status: str
    submitted_at: str

    class Config:
        from_attributes = True
