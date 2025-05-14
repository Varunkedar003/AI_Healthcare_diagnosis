document.getElementById("symptomForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form from refreshing

    const symptoms = document.getElementById("symptoms").value.split(',').map(item => item.trim());
    console.log("Symptoms sent to backend:", symptoms);

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ symptoms: symptoms }),
        });

        const data = await response.json();
        console.log("Response Data:", data);

        // Ensure you're accessing the correct keys
        document.getElementById("diagnosis").innerText = `Diagnosis: ${data.condition}`;
        document.getElementById("recommendations").innerText = `Recommendations: ${data.specific_suggestions.join(", ")}`;
        document.getElementById("treatment").innerText = `Treatment: ${data.treatment}`;

    } catch (error) {
        console.error("Error during fetch:", error);
        document.getElementById("diagnosis").innerText = "An error occurred. Please try again later.";
        document.getElementById("recommendations").innerText = "";
        document.getElementById("treatment").innerText = "";
    }
});
