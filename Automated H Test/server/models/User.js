// const mongoose = require('mongoose')

// const Automated_H_TestSchema = new mongoose.Schema({

//     name: String,
//     email: String,
//     dob: String,
//     password: String,
//     confirmPassword: String

// })

// const Automated_H_TestModel = mongoose.model("Automated_H_Test",Automated_H_TestSchema)
// module.exports = Automated_H_TestModel

const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema(
  {
    name: String,
    email: String,
    dob: String,
    password: String,
    confirmPassword: String,
  },
  { timestamps: true }
);

const UserModel = mongoose.model("User", UserSchema); // Use "User" as the model name
module.exports = UserModel;
