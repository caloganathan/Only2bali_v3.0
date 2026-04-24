import { generateItinerary as apiGenerateItinerary } from './api';

export const getItinerary = async ({ tripId, userPrefs, dates, groupSize, budgetUsd }) => {
  const response = await apiGenerateItinerary({
    trip_id: tripId,
    user_prefs: userPrefs,
    dates,
    group_size: groupSize,
    budget_usd: budgetUsd || null,
  });
  return response.data;
};
