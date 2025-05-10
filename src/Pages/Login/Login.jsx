import React, { useState, useEffect } from "react";
import { useDispatch } from 'react-redux';
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { decodeJwt } from "jose";
import "./Login.css";
import { setAuthenticated } from "../../slices/authSlice";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const user = JSON.parse(localStorage.getItem("user"));
    if (token && user) {
      try {
        const decoded = decodeJwt(token);
        const now = Math.floor(Date.now() / 1000);
        if (decoded.exp > now) {
          dispatch(setAuthenticated(res.data.user));
          navigate("/home");
        } else {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");
        }
      } catch (err) {
        console.error("Invalid token", err);
        localStorage.removeItem("access_token");
      }
    }
  }, [navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      const res = await axios.post("http://localhost:5001/login", form, {
        withCredentials: true
      });

      console.log("###: ", res.data)

      const token = res.data.access_token;
      if (token) {
        localStorage.setItem("access_token", token);
        dispatch(setAuthenticated(res));
      }

      setSuccess("Login successful! Welcome user #" + (res.data.user_id || ""));
      navigate("/home"); // Redirect to your target page
    } catch (err) {
      setError("Login failed: " + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Sign In</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          className="login-input"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          className="login-input"
        />
        <button type="submit" className="login-button">
          Log In
        </button>
      </form>
      {success && <div className="login-success">{success}</div>}
      {error && <div className="login-error">{error}</div>}
    </div>
  );
};

export default Login;