import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .models.database import engine, Base
from .routers import vendors, users, trips, itinerary, pricing, booking

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Only2Bali API v1",
    version="1.0.0",
    description="Only2Bali vendor onboarding and trip planning API",
    lifespan=lifespan,
)

cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,https://polite-sand-0b0ded210.6.azurestaticapps.net",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router, prefix="/api/v1", tags=["Vendors"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(trips.router, prefix="/api/v1", tags=["Trips"])
app.include_router(itinerary.router, prefix="/api/v1", tags=["Itinerary"])
app.include_router(pricing.router, prefix="/api/v1", tags=["Pricing"])
app.include_router(booking.router, prefix="/api/v1", tags=["Booking"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "only2bali-fastapi"}
