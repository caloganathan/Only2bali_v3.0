import axios from 'axios';

const BASE_URL = process.env.REACT_APP_FASTAPI_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

export const createUser = (data) => api.post('/api/v1/users', data);
export const createTrip = (data) => api.post('/api/v1/trips', data);
export const getTrip = (tripId) => api.get(`/api/v1/trips/${tripId}`);
export const generateItinerary = (data) => api.post('/api/v1/generate-itinerary', data);
export const calculatePrice = (data) => api.post('/api/v1/calculate-price', data);
export const matchVendors = (params) => api.get('/api/v1/match-vendors', { params });
export const createBooking = (data) => api.post('/api/v1/create-booking', data);
export const registerVendor = (data) => api.post('/api/v1/vendors/register', data);

export default api;
