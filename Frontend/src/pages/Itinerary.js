import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ItineraryDisplay from "../components/ItineraryDisplay";
import PricingEstimate from "../components/PricingEstimate";
import "./Itinerary.css";

const ItineraryPage = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [showPricing, setShowPricing] = useState(false);

  const tripId = state?.tripId;
  const itinerary = state?.itinerary;

  const days = itinerary?.days?.length || 3;

  const handleProceedToBooking = (totalPrice) => {
    navigate("/booking", {
      state: {
        tripId,
        itineraryId: itinerary?.itinerary_id,
        totalPrice,
      },
    });
  };

  if (!itinerary) {
    return (
      <div className="itp-error">
        <p>No itinerary found. <button onClick={() => navigate("/plan")}>Start Planning</button></p>
      </div>
    );
  }

  return (
    <div className="itp-page">
      <div className="itp-back">
        <button onClick={() => navigate("/plan")}>← Back to Planning</button>
      </div>

      <ItineraryDisplay
        itinerary={itinerary}
        onProceed={() => setShowPricing(true)}
      />

      {showPricing && (
        <div className="itp-pricing-section">
          <PricingEstimate
            tripId={tripId}
            itineraryId={itinerary?.itinerary_id}
            days={days}
            onProceedToBooking={handleProceedToBooking}
          />
        </div>
      )}
    </div>
  );
};

export default ItineraryPage;
