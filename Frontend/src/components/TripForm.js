import React, { useState, useRef } from "react";
import { createUser, createTrip, generateItinerary } from "../services/api";
import "./TripForm.css";

const DIET_OPTIONS = ["Pure Veg", "Jain", "Vegan", "Mixed"];
const INTEREST_OPTIONS = [
  "Adventure",
  "Culture",
  "Food & Dining",
  "Wellness & Spa",
  "Shopping",
  "Beach",
];

const TripForm = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    dateFrom: "",
    dateTo: "",
    groupSize: "",
    budgetUsd: "",
    dietType: "",
    interests: [],
  });

  const step1Ref = useRef(null);
  const step2Ref = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const toggleInterest = (interest) => {
    setFormData((prev) => {
      const exists = prev.interests.includes(interest);
      return {
        ...prev,
        interests: exists
          ? prev.interests.filter((i) => i !== interest)
          : [...prev.interests, interest],
      };
    });
  };

  const handleNext = () => {
    if (currentStep === 1) {
      if (!step1Ref.current.checkValidity()) {
        step1Ref.current.reportValidity();
        return;
      }
      if (formData.dateTo && formData.dateFrom && formData.dateTo < formData.dateFrom) {
        setError("Return date must be after departure date.");
        return;
      }
    }
    if (currentStep === 2) {
      if (!formData.dietType) {
        setError("Please select a diet type.");
        return;
      }
    }
    setCurrentStep((s) => s + 1);
  };

  const handleBack = () => setCurrentStep((s) => s - 1);

  const handleSubmit = async () => {
    setIsLoading(true);
    setError("");
    try {
      const userRes = await createUser({
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
      });
      const userId = userRes.data.id || userRes.data.user_id;

      const tripRes = await createTrip({
        user_id: userId,
        travel_dates: { from: formData.dateFrom, to: formData.dateTo },
        group_size: parseInt(formData.groupSize, 10),
        budget: formData.budgetUsd ? parseFloat(formData.budgetUsd) : null,
        diet: formData.dietType,
      });
      const tripId = tripRes.data.id || tripRes.data.trip_id;

      const itinRes = await generateItinerary({
        trip_id: tripId,
        user_prefs: {
          diet: formData.dietType,
          interests: formData.interests,
        },
        dates: { from: formData.dateFrom, to: formData.dateTo },
        group_size: parseInt(formData.groupSize, 10),
        budget_usd: formData.budgetUsd ? parseFloat(formData.budgetUsd) : null,
      });

      onComplete(tripId, itinRes.data);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Something went wrong. Please try again.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const numDays =
    formData.dateFrom && formData.dateTo
      ? Math.max(
          1,
          Math.round(
            (new Date(formData.dateTo) - new Date(formData.dateFrom)) /
              (1000 * 60 * 60 * 24)
          ) + 1
        )
      : null;

  return (
    <div className="tripform-page">
      <div className="loading-bar-container">
        <div
          className="loading-bar"
          style={{ width: `${Math.round((currentStep / 3) * 100)}%` }}
        ></div>
      </div>

      <div className="tripform-wrapper">
        <div className="tripform-step-indicator">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`step-dot${currentStep === s ? " active" : ""}${
                currentStep > s ? " done" : ""
              }`}
            >
              <span className="step-num">{s}</span>
              <span className="step-label">
                {s === 1 ? "Travel Details" : s === 2 ? "Preferences" : "Confirm"}
              </span>
            </div>
          ))}
        </div>

        {/* STEP 1 */}
        {currentStep === 1 && (
          <form className="tripform-card" ref={step1Ref} noValidate>
            <h2 className="tripform-heading">Step 1 of 3 &mdash; Travel Details</h2>

            <div className="tripform-field">
              <label htmlFor="name">Full Name</label>
              <input
                id="name"
                name="name"
                type="text"
                placeholder="Your full name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="tripform-field">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="tripform-field">
              <label htmlFor="phone">Phone / WhatsApp</label>
              <input
                id="phone"
                name="phone"
                type="tel"
                placeholder="+91 XXXXX XXXXX"
                value={formData.phone}
                onChange={handleChange}
                required
              />
            </div>

            <div className="tripform-row">
              <div className="tripform-field">
                <label htmlFor="dateFrom">Travel Date (From)</label>
                <input
                  id="dateFrom"
                  name="dateFrom"
                  type="date"
                  value={formData.dateFrom}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="tripform-field">
                <label htmlFor="dateTo">Travel Date (To)</label>
                <input
                  id="dateTo"
                  name="dateTo"
                  type="date"
                  value={formData.dateTo}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="tripform-field">
              <label htmlFor="groupSize">Group Size</label>
              <input
                id="groupSize"
                name="groupSize"
                type="number"
                min="1"
                max="50"
                placeholder="Number of travellers"
                value={formData.groupSize}
                onChange={handleChange}
                required
              />
            </div>

            <button type="button" className="tripform-btn" onClick={handleNext}>
              Next &rarr;
            </button>
          </form>
        )}

        {/* STEP 2 */}
        {currentStep === 2 && (
          <form className="tripform-card" ref={step2Ref} noValidate>
            <h2 className="tripform-heading">Step 2 of 3 &mdash; Preferences</h2>

            <div className="tripform-field">
              <label htmlFor="budgetUsd">Approximate Budget (USD)</label>
              <input
                id="budgetUsd"
                name="budgetUsd"
                type="number"
                min="0"
                placeholder="Optional — leave blank if flexible"
                value={formData.budgetUsd}
                onChange={handleChange}
              />
            </div>

            <div className="tripform-field">
              <label>Diet Type <span className="required-star">*</span></label>
              <div className="tripform-card-select">
                {DIET_OPTIONS.map((opt) => (
                  <button
                    type="button"
                    key={opt}
                    className={`select-card-btn${formData.dietType === opt ? " selected" : ""}`}
                    onClick={() => setFormData((prev) => ({ ...prev, dietType: opt }))}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            <div className="tripform-field">
              <label>Interests <span className="hint-text">(select all that apply)</span></label>
              <div className="tripform-card-select">
                {INTEREST_OPTIONS.map((opt) => (
                  <button
                    type="button"
                    key={opt}
                    className={`select-card-btn${
                      formData.interests.includes(opt) ? " selected" : ""
                    }`}
                    onClick={() => toggleInterest(opt)}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            <div className="tripform-btn-row">
              <button type="button" className="tripform-btn-secondary" onClick={handleBack}>
                &larr; Back
              </button>
              <button type="button" className="tripform-btn" onClick={handleNext}>
                Next &rarr;
              </button>
            </div>
          </form>
        )}

        {/* STEP 3 */}
        {currentStep === 3 && (
          <div className="tripform-card">
            <h2 className="tripform-heading">Step 3 of 3 &mdash; Confirm &amp; Generate</h2>

            <div className="tripform-summary">
              <h3 className="summary-title">Trip Summary</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="summary-label">Name</span>
                  <span className="summary-value">{formData.name}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Email</span>
                  <span className="summary-value">{formData.email}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Phone</span>
                  <span className="summary-value">{formData.phone}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Dates</span>
                  <span className="summary-value">
                    {formData.dateFrom} &rarr; {formData.dateTo}
                    {numDays && <span className="days-badge">{numDays} days</span>}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Group Size</span>
                  <span className="summary-value">{formData.groupSize} travellers</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Budget</span>
                  <span className="summary-value">
                    {formData.budgetUsd ? `$${formData.budgetUsd} USD` : "Flexible"}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Diet</span>
                  <span className="summary-value">{formData.dietType}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Interests</span>
                  <span className="summary-value">
                    {formData.interests.length > 0
                      ? formData.interests.join(", ")
                      : "None selected"}
                  </span>
                </div>
              </div>
            </div>

            <div className="tripform-btn-row">
              <button type="button" className="tripform-btn-secondary" onClick={handleBack}>
                &larr; Back
              </button>
              <button
                type="button"
                className="tripform-btn"
                onClick={handleSubmit}
                disabled={isLoading}
              >
                {isLoading ? (
                  <span className="btn-loading">
                    <span className="spinner"></span> Generating...
                  </span>
                ) : (
                  "Generate My Itinerary ✨"
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="popup-overlay">
          <div className="popup">
            <p className="error">{error}</p>
            <button onClick={() => setError("")}>OK</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TripForm;
