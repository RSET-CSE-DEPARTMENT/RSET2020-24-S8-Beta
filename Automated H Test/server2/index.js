const express = require("express");
const WebSocket = require("ws");
const http = require("http");
const cors = require("cors");
const { SerialPort } = require("serialport");
const { ReadlineParser } = require("@serialport/parser-readline");
const mongoose = require("mongoose");

const app = express();
app.use(cors());

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const port = new SerialPort({ path: "COM3", baudRate: 9600 });
const parser = port.pipe(new ReadlineParser({ delimiter: "\r\n" }));

let sendData = false;

app.get("/test", (req, res) => {
  sendData = true;
  res.send("Data sending is triggered");
});

parser.on("data", (data) => {
  console.log(data);
  if (sendData) {
    if (data == 8 || data == 4) {
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(data);
        }
      });

      sendData = false;
    }
  }
});

const connectionString =
  "mongodb+srv://josephtomy02:nypTxnJpT33mUMxx@cluster0.q0pzxp5.mongodb.net/automated_h_test?retryWrites=true&w=majority";

const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  dob: String,
  slotNo: Number,
  status: String,
  result: String,
});

const User = mongoose.model("users", userSchema);

mongoose
  .connect(connectionString, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log(err));

app.use(cors());

app.get("/users", async (req, res) => {
  try {
    const user = await User.find({}).sort({ createdAt: -1 }).limit(1);
    res.json(user);
  } catch (error) {
    console.error("Error retrieving the last created user:", error);
    res.status(500).send(error);
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

const PORT = 8000;
server.listen(PORT, () =>
  console.log(`Server running on http://localhost:${PORT}`)
);
