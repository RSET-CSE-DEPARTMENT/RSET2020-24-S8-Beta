// server.js
const express = require("express");
const cors = require("cors");
const db = require("./db");
const bookingRoutes = require("./booking.routes");

const app = express();
app.use(express.json());
app.use(cors());

// Use booking routes
app.use("/api", bookingRoutes);

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
