import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import './RegistrationForm.css'; // Import CSS file

const RegistrationForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/auth/api/register/",
        formData
      );
      console.log(response.data);
      navigate("/login"); // Redirect to login page on success
    } catch (error) {
      console.error("Registration failed:", error.response.data);
      setError("your credentials are not unique"); // Set error message
    }
  };

  const handleLoginButtonClick = () => {
    navigate("/"); // Navigate to login page
  };

  return (
    <div className="registration-form-container">
      <h2>User Registration</h2>
      {error && <p className="error-message">{error}</p>} {/* Display error message */}
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>
        <button type="submit">Register</button>
      </form>
      <button className="go-to-login-button" onClick={handleLoginButtonClick}>Go to Login Page</button>
    </div>
  );
};

export default RegistrationForm;
