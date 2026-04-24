from enum import Enum
from typing import Optional, List
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


# User schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    preferences: Optional[dict] = None


class UserOut(BaseModel):
    user_id: str
    message: str


# Trip schemas
class TripCreate(BaseModel):
    user_id: str
    travel_date_from: str
    travel_date_to: str
    group_size: int
    budget_usd: Optional[float] = None
    diet_type: Optional[str] = None
    interests: Optional[list] = None

    @field_validator("group_size")
    @classmethod
    def group_size_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("group_size must be greater than 0")
        return v


class TripOut(BaseModel):
    trip_id: str
    status: str
    lead_score: Optional[str]


class TripDetail(BaseModel):
    trip_id: str
    user_id: str
    travel_date_from: str
    travel_date_to: str
    group_size: int
    budget_usd: Optional[float]
    status: str


# Itinerary schemas
class ItineraryRequest(BaseModel):
    trip_id: str
    user_prefs: dict
    dates: dict
    group_size: int
    budget_usd: Optional[float] = None


class DayPlan(BaseModel):
    day: int
    date: str
    activities: list
    meals: dict
    transport: str
    accommodation: str
    estimated_cost_usd: float


class ItineraryOut(BaseModel):
    itinerary_id: str
    trip_id: str
    days: list
    total_estimated_cost_usd: float


# Pricing schemas
class PriceRequest(BaseModel):
    itinerary_id: str
    group_size: int
    price_tier: str


class PriceBreakdown(BaseModel):
    hotel: float
    food: float
    transport: float
    tours: float
    total: float


# Vendor match schemas
class VendorMatch(BaseModel):
    vendor_id: str
    name: str
    type: str
    rating: Optional[float]
    price_tier: str
    veg_type: Optional[str]
    location: str


# Booking schemas
class BookingCreate(BaseModel):
    trip_id: str
    itinerary_id: str
    total_price: float
    notes: Optional[str] = None
    contact_email: str


class BookingOut(BaseModel):
    booking_id: str
    status: str
    confirmation_ref: str
    message: str
