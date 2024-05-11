const mongoose = require("mongoose");

// Replace with your MongoDB connection string
const connectionString =
  "mongodb+srv://josephtomy02:nypTxnJpT33mUMxx@cluster0.q0pzxp5.mongodb.net/automated_h_test?retryWrites=true&w=majority";

// Define your user schema
const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  dob: String,
  password: String,
  confirmPassword: String,
});

const User = mongoose.model("users", userSchema);

async function fetchUsers() {
  try {
    // Connect to MongoDB
    await mongoose.connect(connectionString, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    // Fetch all users
    const users = await User.find({});

    // Log the fetched users
    return users;
  } catch (error) {
    console.error(error);
    return [];
  } finally {
    // Disconnect from MongoDB
    await mongoose.disconnect();
  }
}

module.exports = {
  fetchUsers,
};
