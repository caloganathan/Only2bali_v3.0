import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import TripForm from "../components/TripForm";
import ItineraryDisplay from "../components/ItineraryDisplay";
import "./PlanTrip.css";

const PlanTrip = () => {
  const navigate = useNavigate();
  const [tripId, setTripId] = useState(null);
  const [itinerary, setItinerary] = useState(null);

  const handleTripComplete = (newTripId, itineraryData) => {
    setTripId(newTripId);
    setItinerary(itineraryData);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleProceedToPricing = () => {
    navigate("/itinerary", {
      state: { tripId, itinerary },
    });
  };

  return (
    <div className="pt-page">
      {!itinerary ? (
        <TripForm onComplete={handleTripComplete} />
      ) : (
        <ItineraryDisplay itinerary={itinerary} onProceed={handleProceedToPricing} />
      )}
    </div>
  );
};

export default PlanTrip;
