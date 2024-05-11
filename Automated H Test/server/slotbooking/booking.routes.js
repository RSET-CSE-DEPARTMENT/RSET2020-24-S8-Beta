// booking.routes.js
const express = require('express');
const Booking = require('./booking.model');

const router = express.Router();

// Route to handle booking creation
router.post('/bookings', async (req, res) => {
  console.log("entered in bookings")
  try {
    const { date, slot, username } = req.body;
    const booking = await Booking.create({ date, slot, username });
    res.status(201).json(booking);
  } catch (error) {
    console.error('Error creating booking:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;
