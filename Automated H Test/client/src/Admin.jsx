import React from "react";
import "./login.css";
import { useNavigate } from "react-router-dom";

function Admin() {
  let navigate = useNavigate();

  function handleClick() {
    navigate("/test");
  }
  return (
    <div className="form-container">
      <h2>Login</h2>

      <label>
        User id:
        <input type="email" />
      </label>
      <label>
        Password:
        <input type="password" />
      </label>
      <button onClick={handleClick}>Login</button>
    </div>
  );
}

export default Admin;
