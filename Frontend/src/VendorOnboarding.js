import React, { useState, useRef } from "react";
import "./VendorOnboarding.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CATEGORIES = [
  { value: "Indian Food", emoji: "🍛", label: "Indian Food" },
  { value: "Transport", emoji: "🚗", label: "Transport" },
  { value: "Tour Guide", emoji: "🧭", label: "Tour Guide" },
  { value: "Shopping Souvenirs", emoji: "🛍️", label: "Shopping Souvenirs" },
  { value: "Wooden Products", emoji: "🪵", label: "Wooden Products" },
  { value: "Eatables (Souvenirs)", emoji: "🍬", label: "Eatables (Souvenirs)" },
  { value: "Batik Products", emoji: "🎨", label: "Batik Products" },
];

const PRICE_TIERS = [
  { value: "budget", label: "Budget" },
  { value: "mid", label: "Mid" },
  { value: "premium", label: "Premium" },
];

const FASTAPI_BASE = process.env.REACT_APP_FASTAPI_URL || "http://localhost:8000";

const VendorOnboarding = () => {
  const navigate = useNavigate();
  const formRef = useRef(null);

  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedTier, setSelectedTier] = useState("");
  const [form, setForm] = useState({
    business_name: "",
    contact_person: "",
    email: "",
    whatsapp: "",
    location_bali: "",
    description: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleInput = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedCategory) {
      setError("Please select a vendor category.");
      return;
    }
    if (!selectedTier) {
      setError("Please select a price tier.");
      return;
    }
    if (!formRef.current.checkValidity()) {
      formRef.current.reportValidity();
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(
        `${FASTAPI_BASE}/api/v1/vendors/register`,
        {
          business_name: form.business_name,
          category: selectedCategory,
          contact_person: form.contact_person,
          email: form.email,
          whatsapp: form.whatsapp,
          location_bali: form.location_bali,
          price_tier: selectedTier,
          description: form.description || null,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      if (response.status === 201) {
        setSuccess(response.data.message);
      }
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : "Something went wrong. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="vo-container">
      <div className="loading-bar-container">
        <div className="loading-bar" style={{ width: "100%" }}></div>
      </div>

      <h1 className="vo-h1">Register as a Vendor Partner</h1>
      <p className="vo-p">
        Join our network of trusted Bali service providers. Select your category
        and fill in your details — our team will reach out within 2-3 business
        days.
      </p>

      {/* Category Selection */}
      <div className="vo-category-grid">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.value}
            type="button"
            className={`vo-cat-btn ${selectedCategory === cat.value ? "selected" : ""}`}
            onClick={() => {
              setSelectedCategory(cat.value);
              setError("");
            }}
          >
            <span className="vo-cat-emoji">{cat.emoji}</span>
            <span className="vo-cat-label">{cat.label}</span>
            {selectedCategory === cat.value && (
              <span className="vo-cat-check">✓</span>
            )}
          </button>
        ))}
      </div>

      {/* Registration Form */}
      <form ref={formRef} className="vo-form" onSubmit={handleSubmit} noValidate>
        <div className="vo-form-grid">
          <div className="vo-field">
            <label className="vo-label">Business / Vendor Name</label>
            <input
              className="vo-input"
              type="text"
              name="business_name"
              value={form.business_name}
              onChange={handleInput}
              placeholder="e.g. Bali Spice Kitchen"
              required
            />
          </div>

          <div className="vo-field">
            <label className="vo-label">Contact Person Name</label>
            <input
              className="vo-input"
              type="text"
              name="contact_person"
              value={form.contact_person}
              onChange={handleInput}
              placeholder="e.g. Wayan Sari"
              required
            />
          </div>

          <div className="vo-field">
            <label className="vo-label">Email Address</label>
            <input
              className="vo-input"
              type="email"
              name="email"
              value={form.email}
              onChange={handleInput}
              placeholder="e.g. vendor@email.com"
              required
            />
          </div>

          <div className="vo-field">
            <label className="vo-label">WhatsApp Number</label>
            <input
              className="vo-input"
              type="tel"
              name="whatsapp"
              value={form.whatsapp}
              onChange={handleInput}
              placeholder="e.g. +62 812 3456 7890"
              required
            />
          </div>

          <div className="vo-field">
            <label className="vo-label">Location in Bali</label>
            <input
              className="vo-input"
              type="text"
              name="location_bali"
              value={form.location_bali}
              onChange={handleInput}
              placeholder="e.g. Seminyak, Ubud, Kuta"
              required
            />
          </div>

          {/* Price Tier */}
          <div className="vo-field">
            <label className="vo-label">Price Tier</label>
            <div className="vo-tier-group">
              {PRICE_TIERS.map((tier) => (
                <button
                  key={tier.value}
                  type="button"
                  className={`vo-tier-btn ${selectedTier === tier.value ? "selected" : ""}`}
                  onClick={() => {
                    setSelectedTier(tier.value);
                    setError("");
                  }}
                >
                  {tier.label}
                </button>
              ))}
            </div>
          </div>

          <div className="vo-field vo-field-full">
            <label className="vo-label">Description of Services</label>
            <textarea
              className="vo-input vo-textarea"
              name="description"
              value={form.description}
              onChange={handleInput}
              placeholder="Briefly describe what you offer, specialties, and why travellers should choose you..."
              rows={4}
            />
          </div>
        </div>

        <div className="vo-actions">
          <button
            type="button"
            className="vo-back-btn"
            onClick={() => navigate(-1)}
            disabled={isLoading}
          >
            ← Back
          </button>
          <button type="submit" className="vo-submit-btn" disabled={isLoading}>
            {isLoading ? "Submitting..." : "Submit Registration"}
          </button>
        </div>
      </form>

      {/* Error Popup */}
      {error && (
        <div className="popup-overlay">
          <div className="popup">
            <p className="error">{error}</p>
            <button onClick={() => setError("")}>OK</button>
          </div>
        </div>
      )}

      {/* Success Popup */}
      {success && (
        <div className="popup-overlay">
          <div className="popup popup-success">
            <p className="vo-success-msg">{success}</p>
            <button
              onClick={() => {
                setSuccess("");
                navigate("/");
              }}
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VendorOnboarding;
