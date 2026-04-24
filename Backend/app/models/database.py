import uuid
import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Text, DateTime,
    Integer, Boolean, Date, Numeric, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./only2bali.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class VendorOnboarding(Base):
    __tablename__ = "vendor_onboarding"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    whatsapp = Column(String(20), nullable=False)
    location_bali = Column(String(100), nullable=False)
    price_tier = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    submitted_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    preferences = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    travel_date_from = Column(Date, nullable=False)
    travel_date_to = Column(Date, nullable=False)
    group_size = Column(Integer, nullable=False)
    budget_usd = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), default="draft")
    lead_score = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="trips")
    itineraries = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="trip", cascade="all, delete-orphan")


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    veg_type = Column(String(20), nullable=True)
    location = Column(String(100), nullable=False)
    rating = Column(Numeric(2, 1), nullable=True)
    price_tier = Column(String(10), nullable=False)


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String(36), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    plan = Column(Text, nullable=False)
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="itineraries")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String(36), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), default="pending")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="bookings")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
