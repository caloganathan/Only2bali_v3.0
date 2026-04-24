import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import BookingForm from "../components/BookingForm";
import "./Booking.css";

const BookingPage = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [confirmationRef, setConfirmationRef] = useState(null);

  const tripId = state?.tripId;
  const itineraryId = state?.itineraryId;
  const totalPrice = state?.totalPrice;

  const handleSuccess = (ref) => {
    setConfirmationRef(ref);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (confirmationRef) {
    return (
      <div className="bkp-page">
        <div className="bkp-confirmed-card">
          <div className="bkp-checkmark">✅</div>
          <h2 className="bkp-confirmed-title">Booking Confirmed!</h2>
          <p className="bkp-confirmed-ref">Reference: <strong>{confirmationRef}</strong></p>
          <p className="bkp-confirmed-msg">
            Our team will contact you within 24 hours to finalise your Bali itinerary.
          </p>
          <button className="bkp-home-btn" onClick={() => navigate("/")}>
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bkp-page">
      <BookingForm
        tripId={tripId}
        itineraryId={itineraryId}
        totalPrice={totalPrice}
        onSuccess={handleSuccess}
      />
    </div>
  );
};

export default BookingPage;
