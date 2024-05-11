import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login({ setUsername }) {
  const [username, setUsernameLocal] = useState("");
  const [password, setPassword] = useState("");
  const [isValid, setIsValid] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    // Check if email and password are filled
    if (!username || !password) {
      window.alert("Please fill in all fields"); // Show pop-up message if fields are not filled
      return;
    }

    // Perform email validation
    // const emailRegex = /^[^\s@]+@gmail\.com$/; // Regular expression for Gmail format validation
    // if (!emailRegex.test(email)) {
    //   window.alert("Invalid Gmail format"); // Show pop-up message for invalid Gmail format
    //   return;
    // }

    // Perform authentication logic here
    // For demonstration, let's assume authentication is successful if email is not empty

    if (username.trim() !== "") {
      // Navigate to the specified route if authentication is successful
      setUsername(username);
      axios
        .get(
          `http://localhost:3001/verifyUser?username=${username}&password=${password}`
        )
        .then((response) => {
          console.log("Recieved User Details");
          console.log(response.data);
          if (response.data) {
            navigate("/loginSignup/slot");
          } else {
            setIsValid(true);
          }
        })
        .catch((error) => {
          console.log("Error", error);
        });
    } else {
      // Handle authentication failure (e.g., display error message)
      console.log("Authentication failed: Username is empty");
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      <label>
        Username:
        <input
          type="username"
          value={username}
          onChange={(e) => {
            setUsernameLocal(e.target.value);
          }}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      {isValid && <div>Invalid username or password</div>}
      <button onClick={handleClick}>Login</button>
    </div>
  );
}

export default Login;
