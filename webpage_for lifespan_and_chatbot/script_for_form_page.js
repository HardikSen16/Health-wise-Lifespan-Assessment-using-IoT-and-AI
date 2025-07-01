
    function calculateBMI() {
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);

    if (!height || !weight || height < 50 || weight < 10) {
        alert("Please enter valid height and weight.");
        return;
    }

    const heightInMeters = height / 100;
    const bmi = weight / (heightInMeters * heightInMeters);
    const roundedBMI = bmi.toFixed(2);

    document.getElementById("bmi").value = roundedBMI;
}

        // Firebase Realtime Database URL
        const databaseURL = "https://wellspan-ec001-default-rtdb.firebaseio.com"; // Replace with your Database URL

        // Fetch data from Firebase and populate the form
        async function populateFormWithFirebaseData() {
            try {
                // Fetch data from the /health node using the REST API
                const response = await fetch(`${databaseURL}/health.json`);
                const data = await response.json(); // Parse the JSON response

                // Populate form fields with Firebase data
                if (data) {
                    document.getElementById("heartRate").value = data.BPM || "";
                    document.getElementById("spo2").value = data.SpO2 || "";
                    document.getElementById("temperature").value = data.Temperature || "";
                }
            } catch (error) {
                console.error("Error fetching data from Firebase:", error);
                alert("Failed to fetch data from Firebase. Please try again.");
            }
        }

        // Open the popup form
        function openForm() {
            document.getElementById("popup").style.display = "block";
        }

        // Close the popup form
        function closeForm() {
            document.getElementById("popup").style.display = "none";
        }

        // Call the function to populate the form when the page loads
        //window.onload = populateFormWithFirebaseData;

        // Handle form submission
        document.getElementById("predictionForm").addEventListener("submit", async function(event) {
            event.preventDefault(); // Prevent form from reloading the page

            let data = {
                age: document.getElementById("age").value,
                country: document.getElementById("country").value,
                gender: document.getElementById("gender").value,
                exercise: document.getElementById("exercise").value,
                diet: document.getElementById("diet").value,
                medical: document.getElementById("medical").value,
                stress: document.getElementById("stress").value,
                smoking: document.getElementById("smoking").value,
                alcohol: document.getElementById("alcohol").value,
                social: document.getElementById("social").value,
                bmi: document.getElementById("bmi").value,
                sleep: document.getElementById("sleep").value,
                heartRate: document.getElementById("heartRate").value,
                spo2: document.getElementById("spo2").value,
                temperature: document.getElementById("temperature").value
            };

            try {
                let response = await fetch("http://127.0.0.1:8000/predict", { // make sure this matches your FastAPI port
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });

                let result = await response.json();

                // Store both in sessionStorage
        sessionStorage.setItem("prediction", result.predicted_life_expectancy);
        sessionStorage.setItem("initial_message", result.initial_message);

        // Redirect
        window.location.href = "prediction_chat.html";
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to get prediction. Please try again.");
    }
        });