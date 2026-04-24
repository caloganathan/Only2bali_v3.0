from ..models.database import Vendor


def match_vendors(
    db,
    vendor_type: str = None,
    veg_type: str = None,
    location: str = None,
    price_tier: str = None,
) -> list:
    query = db.query(Vendor)
    if vendor_type:
        query = query.filter(Vendor.type == vendor_type)
    if veg_type:
        query = query.filter(Vendor.veg_type == veg_type)
    if location:
        query = query.filter(Vendor.location.ilike(f"%{location}%"))
    if price_tier:
        query = query.filter(Vendor.price_tier == price_tier)
    vendors = query.all()
    vendors.sort(key=lambda v: (v.rating or 0), reverse=True)
    return vendors
