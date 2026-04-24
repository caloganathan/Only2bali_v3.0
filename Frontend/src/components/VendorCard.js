import React from "react";
import "./VendorCard.css";

const TIER_CONFIG = {
  budget: { label: "Budget", color: "#22c55e", dot: "🟢" },
  mid: { label: "Mid", color: "#eab308", dot: "🟡" },
  premium: { label: "Premium", color: "#ef4444", dot: "🔴" },
};

const TYPE_COLORS = {
  "Indian Food": "#f97316",
  Transport: "#3b82f6",
  "Tour Guide": "#8b5cf6",
  "Shopping Souvenirs": "#ec4899",
  "Wooden Products": "#a16207",
  "Eatables (Souvenirs)": "#10b981",
  "Batik Products": "#6366f1",
};

const VendorCard = ({ vendor }) => {
  if (!vendor) return null;

  const tier = vendor.price_tier ? vendor.price_tier.toLowerCase() : "budget";
  const tierInfo = TIER_CONFIG[tier] || TIER_CONFIG.budget;
  const typeColor = TYPE_COLORS[vendor.category] || "#4EBB87";

  const rating = typeof vendor.rating === "number" ? vendor.rating : 0;
  const maxStars = 5;

  const vegLabel = vendor.veg_type || vendor.diet || null;

  return (
    <div className="vc-card">
      <div className="vc-top-row">
        <div>
          <h3 className="vc-name">{vendor.business_name || vendor.name || "Vendor"}</h3>
          <p className="vc-location">{vendor.location_bali || vendor.location || ""}</p>
        </div>
        <div className="vc-badges-col">
          <span
            className="vc-type-badge"
            style={{ backgroundColor: typeColor }}
          >
            {vendor.category || vendor.type || "Service"}
          </span>
          <span className="vc-tier-badge">
            {tierInfo.dot} {tierInfo.label}
          </span>
        </div>
      </div>

      <div className="vc-rating-row">
        <div className="vc-stars">
          {Array.from({ length: maxStars }).map((_, i) => (
            <span
              key={i}
              className={`vc-star ${i < Math.round(rating) ? "vc-star-filled" : "vc-star-empty"}`}
            >
              &#9679;
            </span>
          ))}
        </div>
        {rating > 0 && (
          <span className="vc-rating-num">{rating.toFixed(1)}</span>
        )}
      </div>

      {vendor.description && (
        <p className="vc-desc">{vendor.description}</p>
      )}

      <div className="vc-footer">
        {vegLabel && (
          <span className="vc-veg-tag">
            <span className="vc-leaf">🌿</span> {vegLabel}
          </span>
        )}
        {vendor.whatsapp && (
          <a
            href={`https://wa.me/${vendor.whatsapp.replace(/[^0-9]/g, "")}`}
            target="_blank"
            rel="noopener noreferrer"
            className="vc-whatsapp-link"
          >
            WhatsApp
          </a>
        )}
      </div>
    </div>
  );
};

export default VendorCard;
