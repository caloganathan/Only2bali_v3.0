import React from "react";
import { useNavigate } from "react-router-dom";
import "./HeroSection.css";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <div className="hero-section">
      <div className="hero-overlay"></div>
      <div className="hero-content">
        <div className="hero-glass-card">
          <div className="loading-bar-container">
            <div className="loading-bar" style={{ width: "20%" }}></div>
          </div>
          <h1 className="hero-title">Plan Your Perfect Bali Journey</h1>
          <p className="hero-subtitle">
            AI-powered itineraries tailored for Indian travellers
          </p>
          <button
            className="hero-cta-btn"
            onClick={() => navigate("/plan")}
          >
            Start Planning
          </button>
          <p className="hero-tagline">
            Vegetarian-friendly &nbsp;·&nbsp; Trusted vendors &nbsp;·&nbsp; Instant itinerary
          </p>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
