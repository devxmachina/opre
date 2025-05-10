// src/slices/authSlice.js
import { createSlice } from "@reduxjs/toolkit";

const authSlice = createSlice({
  name: "auth",
  initialState: { 
    authenticated: false,
    user: null,
  },
  reducers: {
    setAuthenticated: (state, action) => {
      state.authenticated = true;
      state.user = action.payload;
    },
    logout: (state) => {
      state.authenticated = false;
      state.user = null;
    }
  }
});

export const { setAuthenticated, logout } = authSlice.actions;
export default authSlice.reducer;