//<script type="module">
  // Import the functions you need from the SDKs you need
 
  //import { initializeApp } from "firebase/app";
  //import { getAnalytics } from "firebase/analytics";
  //import { getDatabase, ref, orderByChild, equalTo, get } from "firebase/database";
  
  var firebase = require("firebase/app");
  require("firebase/analytics");
  require("firebase/database");

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  var firebaseConfig = {
  apiKey: "AIzaSyAdUcuS0qz71dwajrpVcbuRoQtPMT2ShLc",
  authDomain: "fine-payment-9ad2b.firebaseapp.com",
  databaseURL: "https://fine-payment-9ad2b-default-rtdb.firebaseio.com",
  projectId: "fine-payment-9ad2b",
  storageBucket: "fine-payment-9ad2b.appspot.com",
  messagingSenderId: "112719631313",
  appId: "1:112719631313:web:184f36666309923abdc6f0",
  measurementId: "G-Q6KX6W1KHZ"
};

  // Initialize Firebase
  var app = firebase.initializeApp(firebaseConfig);
  var analytics = firebase.getAnalytics(app);

  // Function to handle login process
  function login() {
      var numberPlate = document.getElementById('numberPlate').value;

      // Get a reference to the database service
      var database = getDatabase(app);

      // Get reference to 'numberPlates' node in the database
      var numberPlatesRef = ref(database, 'numberPlates');

      // Query the database to find number plate 1
      var query = orderByChild(ref(numberPlatesRef), 'numberPlates');
      var numberPlateQuery = equalTo(query, numberPlate);

      // Retrieve number plate data based on the query
      get(numberPlateQuery).then((snapshot) => {
          if (snapshot.exists()) {
              // Number plate exists
              console.log("Number plate found:", snapshot.val());
              // Redirect to dashboard page
              window.location.href = "dashboard.html";
          } else {
              console.error("Number plate not found");
              // Display error message to the user if needed
          }
      }).catch((error) => {
          console.error("Error retrieving number plate data:", error);
          // Handle error
      });
  }
//</script>
