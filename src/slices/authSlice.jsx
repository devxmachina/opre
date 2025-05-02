// src/slices/authSlice.js
import { createSlice } from "@reduxjs/toolkit";

const authSlice = createSlice({
  name: "auth",
  initialState: { authenticated: false },
  reducers: {
    setAuthenticated: (state, action) => {
      state.authenticated = action.payload;
    },
    logout: (state) => {
      state.authenticated = false;
    }
  }
});

export const { setAuthenticated, logout } = authSlice.actions;
export default authSlice.reducer;