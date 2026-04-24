import uuid
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vendor_onboarding.db")

# SQLite compatibility: UUID stored as String for SQLite fallback
if DATABASE_URL.startswith("sqlite"):
    from sqlalchemy import String as UUIDType
    uuid_col = lambda: Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
else:
    uuid_col = lambda: Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
