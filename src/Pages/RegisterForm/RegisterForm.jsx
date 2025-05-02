import React, { useState } from "react";
import axios from "axios";
import "./RegisterForm.css";

const RegisterForm = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    profile: "",
    password: ""
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const checkEmail = async (email) => {
    try {
      const res = await axios.get(`http://localhost:5001/check-email?email=${encodeURIComponent(email)}`, {
        withCredentials: true
      });
      return res.data.exists;
    } catch (err) {
      console.error("Email check failed:", err);
      return false; // fallback: assume not taken if check fails
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const emailTaken = await checkEmail(form.email);
    if (emailTaken) {
      setError("This email is already registered.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5001/register", form, {
        withCredentials: true
      });
      setResult(res.data);
      setError(null);
    } catch (err) {
      setError("Registration failed: " + (err.response?.data?.message || err.message));
      setResult(null);
    }
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Sign Up</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={form.name}
          onChange={handleChange}
          required
          className="register-input"
        />
        <input
          type="email"
          name="email"
          placeholder="Email Address"
          value={form.email}
          onChange={handleChange}
          required
          className="register-input"
        />
        <input
          type="text"
          name="profile"
          placeholder="Profile Info (Optional)"
          value={form.profile}
          onChange={handleChange}
          className="register-input"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          className="register-input"
        />
        <button type="submit" className="register-button">
          Create Account
        </button>
      </form>

      {result && (
        <div className="register-success">
          Registration success: Welcome {result.name}!
        </div>
      )}
      {error && <div className="register-error">{error}</div>}
    </div>
  );
};

export default RegisterForm;
