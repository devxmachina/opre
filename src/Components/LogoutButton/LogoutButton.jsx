import React from "react";
import { useNavigate } from "react-router-dom";
import "./LogoutButton.css";

import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../slices/authSlice';

const LogoutButton = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    dispatch(logout());
    navigate("/login");
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Log Out
    </button>
  );
};

export default LogoutButton;