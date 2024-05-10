function runFireDetection() {
    fetch('/fire_detection_script', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById("fire-detection-result").innerText = data.message;
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Check if username and password match your criteria
    // For demonstration, using a simple condition (e.g., username: "user", password: "pass")
    if (username === "user" && password === "pass") {
        // If login is successful, redirect to another page
        window.location.href = "{{ url_for('templates', filename='index.html') }}";
        return false; // Prevents the form from submitting (since it's just for demonstration)
    } else {
        alert("Invalid username or password. Please try again.");
        return false;
    }
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    document.getElementById(tabName).style.display = "block";
   
}

function toggleCameraTabs() {
    var content = document.querySelector('.content');
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

function openSubTab(evt, tabName) {
    var i, subtabcontent, subtablinks;

    subtabcontent = document.getElementsByClassName("subtabcontent");
    for (i = 0; i < subtabcontent.length; i++) {
        subtabcontent[i].style.display = "none";
    }

    document.getElementById(tabName).style.display = "block";
    if (tabName === "camera4") {
        startWebcam();
    }
}

function logout() {
    // Perform logout actions if needed (e.g., clear session data)
    // For now, this function is just redirecting to the login page
    window.location.assign("login.html"); // Redirect to the login page
}

function startWebcam() {
    var video = document.getElementById("webcam");

    // Check if the user's browser supports getUserMedia
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Access the webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                // Display the webcam stream in the video element
                video.srcObject = stream;
            })
            .catch(function (error) {
                console.error('Error accessing webcam: ', error);
            });
    } else {
        console.error('getUserMedia not supported on your browser');
    }
}


