import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./slotbooking.css"; // Import your CSS file
import axios from "axios";
import { backendBaseUrl } from "./utils/urls";

const BookingSlot = ({ username }) => {
  // State to keep track of selected date and slot
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingMessage, setBookingMessage] = useState("");
  const randomNumber = Math.floor(Math.random() * 5); 


  // Array of available slots
  const slots = [
    { time: "9am", id: 1 },
    { time: "10am", id: 2 },
    { time: "11am", id: 3 },
    { time: "2pm", id: 4 },
    { time: "3pm", id: 5 },
  ];

  // Function to handle slot selection
  const handleSlotSelect = (slotId) => {
    setSelectedSlot(slotId);
  };

  // Function to handle booking
  const handleBooking = async () => {
    if (selectedSlot) {
      // Prepare the booking data to send to the backend
      const bookingData = {
        date: selectedDate,
        slot: selectedSlot,
        username,
      };

      console.log("bookingData", bookingData);
      await axios
        .post(`${backendBaseUrl}/api/bookings/`, bookingData)
        .then((response) => {
          setBookingMessage(`Slot ${selectedSlot} booked successfully!`);
          setSelectedSlot(null);
        })
        .catch((error) => {
          console.error("Error booking slot:", error);
          setBookingMessage("Failed to book slot. Please try again later.");
        });
    }
  };

  return (
    <div className="booking-slot-container">
      <h2>Date Selection</h2>
      <div className="date-picker-container">
        <DatePicker
          selected={selectedDate}
          onChange={(date) => setSelectedDate(date)}
          dateFormat="yyyy-MM-dd"
          placeholderText="Select a date"
          className="date-picker"
        />
      </div>

      {/* Time Slot Selection */}
      {selectedDate && (
        <div>
          <h2>Available Slots for {selectedDate.toLocaleDateString()}</h2>
          <div className="slots">
            {slots.map((slot) => (
              <div
                key={slot.id}
                className={`slot ${
                  selectedSlot === slot.id ? "selected" : ""
                } slot ${selectedSlot === randomNumber ? "booked" : ""}`}
                onClick={() => handleSlotSelect(slot.id)}
              >
                {slot.time}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Booking Button */}
      {selectedSlot && (
        <div className="book-button-container">
          <button className="book-button" onClick={handleBooking}>
            Book
          </button>
        </div>
      )}

      {/* Booking Message */}
      {bookingMessage && (
        <div className="booking-message">{bookingMessage}</div>
      )}
    </div>
  );
};

export default BookingSlot;
