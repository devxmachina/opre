import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { decodeJwt } from "jose";
import "./Login.css";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = decodeJwt(token);
        const now = Math.floor(Date.now() / 1000);
        if (decoded.exp > now) {
          setAuthenticated(true);
          navigate("/home");
        } else {
          localStorage.removeItem("access_token");
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

      const token = res.data.access_token;
      if (token) {
        localStorage.setItem("access_token", token);
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