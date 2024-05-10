// // // const express = require('express')
// // // const bodyParser = require('body-parser')
// // // const mongoose = require('mongoose')
// // // var cors = require('cors')
// // // const server = require('./backend/Controller/user')
// // // const app = express()
// // // const config = require('./backend/Config/db_config')



// // // app.use(bodyParser.json())
// // // app.use(bodyParser.urlencoded({ extended: true }))

// // // mongoose
// // //   .connect(
// // //     config.MongoURI,
// // //   )
// // //   .then(() => console.log('MongoDB Connected'))
// // //   .catch((err) => console.log(err))
// // // var port = process.env.PORT || 3001
// // // //var cors = require('cors')

// // // const corsOptions = {
// // //   origin: 'http://localhost:3000',
// // //   credentials: true,            //access-control-allow-credentials:true
// // //   optionSuccessStatus: 200,
// // //   allowedHeaders: ['Authorization']
// // // }
// // // app.use(cors(corsOptions));

// // // app.use('/', server)



// // // app.listen(port)
// // // console.log('App is running on port ' + port)
// // // const express = require('express');
// // // const cors = require('cors');
// // // const fetch = require('node-fetch'); // Install node-fetch package

// // // const app = express();
// // // const PORT = process.env.PORT || 3001;

// // // app.use(cors());

// // // // Define a route to proxy requests to Pinata
// // // app.get('/proxy', async (req, res) => {
// // //   try {
// // //     const ipfsHash = req.query.ipfsHash;
// // //     if (!ipfsHash) {
// // //       return res.status(400).send('IPFS hash is required');
// // //     }

// // //     const response = await fetch(`https://silver-adorable-ocelot-850.mypinata.cloud/ipfs/${ipfsHash}`);
// // //     const data = await response.text();
// // //     console.log('Fetched data:', data);
// // //     res.send(data);
// // //   } catch (error) {
// // //     console.error('Error proxying request:', error);
// // //     res.status(500).send('Internal Server Error');
// // //   }
// // // });

// // // app.listen(PORT, () => {
// // //   console.log(`Server is running on port ${PORT}`);
// // // });
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');
const fetch = require('node-fetch');
const server = require('./backend/Controller/user');
const config = require('./backend/Config/db_config');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// MongoDB Connection
mongoose.connect(config.MongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.error('MongoDB connection error:', err));

// CORS Configuration
const corsOptions = {
  origin: 'http://localhost:3000',
  credentials: true,
  optionSuccessStatus: 200,
  allowedHeaders: ['Authorization', 'Content-Type']
};
app.use(cors(corsOptions));
//app.use(cors());
// Proxy Route
app.get('/proxy', async (req, res) => {
  try {
    const ipfsHash = req.query.ipfsHash;
    if (!ipfsHash) {
      return res.status(400).send('IPFS hash is required');
    }
    const pinataGatewayToken = 'i47fCpinbNBylPNQWk-mw04o21mXpNImgOW6e3w347ZG1QCk_szXUR9eg11SWJWu'; // Replace with your Pinata gateway access token
    const response = await fetch(`https://silver-adorable-ocelot-850.mypinata.cloud/ipfs/${ipfsHash}?pinataGatewayToken=${pinataGatewayToken}`);
    const data = await response.text();
    //console.log('Fetched data:', data);
    res.send(data);
  } catch (error) {
    console.error('Error proxying request:', error);
    res.status(500).send('Internal Server Error');
  }
});

// Routes
app.use('/', server);

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
// // Import necessary modules
// const express = require('express');
// const bodyParser = require('body-parser');
// const mongoose = require('mongoose');
// const cors = require('cors');
// const fetch = require('node-fetch');
// const server = require('./backend/Controller/user');
// const config = require('./backend/Config/db_config');

// // Initialize Express app
// const app = express();
// const PORT = process.env.PORT || 3001;

// // Middleware
// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: true }));

// // MongoDB Connection
// mongoose.connect(config.MongoURI, {
//   useNewUrlParser: true,
//   useUnifiedTopology: true,
// })
//   .then(() => console.log('MongoDB Connected'))
//   .catch(err => console.error('MongoDB connection error:', err));

// // CORS Configuration
// const corsOptions = {
//   origin: 'http://localhost:3000',
//   credentials: true,
//   optionSuccessStatus: 200,
//   allowedHeaders: ['Authorization']
// };
// app.use(cors(corsOptions));

// // Proxy Route
// app.get('/proxy', async (req, res) => {
//   try {
//     const ipfsHash = req.query.ipfsHash;
//     if (!ipfsHash) {
//       return res.status(400).send('IPFS hash is required');
//     }
//     const pinataGatewayToken = 'i47fCpinbNBylPNQWk-mw04o21mXpNImgOW6e3w347ZG1QCk_szXUR9eg11SWJWu'; // Replace with your Pinata gateway access token
//     const response = await fetch(`https://silver-adorable-ocelot-850.mypinata.cloud/ipfs/${ipfsHash}?pinataGatewayToken=${pinataGatewayToken}`);
//     const data = await response.text();
//     console.log('Fetched data:', data);
//     res.send(data);
//   } catch (error) {
//     console.error('Error proxying request:', error);
//     res.status(500).send('Internal Server Error');
//   }
// });

// // Login Route
// app.post('/login', (req, res) => {
//   const { username, password, enterKey } = req.body;

//   // Check the username, password, and enterKey here
//   // Perform authentication logic
//   // For simplicity, let's assume authentication is successful if username, password, and enterKey are not empty
//   if (username && password && enterKey) {
//     // Return a success response
//     res.status(200).json({ message: 'Login successful' });
//   } else {
//     // Return an error response
//     res.status(401).json({ message: 'Invalid credentials' });
//   }
// });

// // Routes
// app.use('/', server);

// // Start the server
// app.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });
