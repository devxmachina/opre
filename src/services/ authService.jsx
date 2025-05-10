// src/services/authService.js
import axios from "axios";

const API_BASE = "http://localhost:5001"; // 필요시 환경변수로 분리

export const loginUser = async (formData) => {
  const response = await axios.post(`${API_BASE}/login`, formData, {
    withCredentials: true,
  });
  return response.data;
};

export const logoutUser = async () => {
  const response = await axios.post(`${API_BASE}/logout`, {}, {
    withCredentials: true,
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await axios.get(`${API_BASE}/me`, {
    withCredentials: true,
  });
  return response.data;
};