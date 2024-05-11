import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Signup({ setUsername }) {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    dob: "",
    password: "",
    confirmPassword: "",
    aadharNumber: "", // Add Aadhar card number field to formData
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    // Validation: Check if all fields are filled
    // if (!formData.name || !formData.email || !formData.dob || !formData.password || !formData.confirmPassword || !formData.aadharNumber) {
    //   setError('All fields are required');
    //   return;
    // }
    // // Validation: Check if passwords match
    // if (formData.password !== formData.confirmPassword) {
    //   setError('Passwords do not match');
    //   return;
    // }
    // // Validation: Check if DOB is valid (you may implement more complex validation logic)
    // const dobRegex = /^\d{4}-\d{2}-\d{2}$/;
    // if (!dobRegex.test(formData.dob)) {
    //   setError('Invalid date of birth format (YYYY-MM-DD)');
    //   return;
    // }
    // // Validation: Check if email is valid
    // const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // if (!emailRegex.test(formData.email)) {
    //   setError('Invalid email format');
    //   return;
    // }
    // // Validation: Check if password contains characters, numbers, and special characters
    // const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
    // if (!passwordRegex.test(formData.password)) {
    //   setError('Password must contain at least one letter, one number, and one special character');
    //   return;
    // }

    try {
      // Perform signup logic here (e.g., send signup request to server)
      setUsername(formData.name);
      const response = await axios.post(
        "http://localhost:3001/users",
        formData
      );
      console.log(response.data); // handle success response here
      navigate("/loginSignup/slot"); // navigate after successful signup
    } catch (error) {
      console.error("Error signing up:", error); // handle error here
    }
  };

  return (
    <div className="form-container">
      <h2>SignUp</h2>

      <label>
        Name:
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
        />
      </label>
      <label>
        Email:
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          pattern="[^\s@]+@[^\s@]+\.[^\s@]+"
          title="Please enter a valid email address"
        />
      </label>
      <label>
        DOB:
        <input
          type="date"
          name="dob"
          value={formData.dob}
          onChange={handleChange}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          pattern=".{6,}"
          title="Password must be at least 6 characters long"
        />
      </label>
      <label>
        Confirm Password:
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
        />
      </label>
      <label>
        Aadhar Card Number:
        <input
          type="text"
          name="aadharNumber"
          value={formData.aadharNumber}
          onChange={handleChange}
        />
      </label>
      {error && <p className="error-message">{error}</p>}
      <button onClick={handleSubmit}>SignUp</button>
    </div>
  );
}

export default Signup;
