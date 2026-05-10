import axios from 'axios';
import type { Farm, AIPrediction, PredictionResponse, WeatherData } from '../types';

const API_BASE_URL = 'https://agrointel-backend-q8mq.onrender.com/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchFarms = async (): Promise<Farm[]> => {
  const { data } = await api.get('/farms/');
  return data;
};

export const runForecast = async (farmId: string): Promise<PredictionResponse> => {
  const { data } = await api.post(`/forecast/run/${farmId}`);
  return data;
};

export const fetchLatestForecast = async (farmId: string): Promise<PredictionResponse> => {
  const { data } = await api.get(`/forecast/latest/${farmId}`);
  return data;
};

export const fetchForecastHistory = async (farmId: string, limit = 10): Promise<AIPrediction[]> => {
  const { data } = await api.get(`/forecast/history/${farmId}?limit=${limit}`);
  return data;
};

export const fetchWeatherHistory = async (farmId: string, limit = 168): Promise<WeatherData[]> => {
  // We'll mock this for now or assume an endpoint exists in the backend for environment
  // Let's assume we create an endpoint to fetch weather history later, or we use a placeholder.
  return [];
};
