document.addEventListener('DOMContentLoaded', () => {

    const appointmentForm = document.getElementById('appointmentForm');
    const doctorSuggestions = document.getElementById('doctorSuggestions');
    const appointmentDetails = document.getElementById('appointmentDetails');
    const selectedDoctor = document.getElementById('selectedDoctor');
    const bookingForm = document.getElementById('bookingForm');

    let selectedDoctorId = null;

    // 🔍 Find Doctors
    appointmentForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const symptoms = document.getElementById('symptoms').value;

        const response = await fetch('/suggest-doctors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms })
        });

        const doctors = await response.json();

        doctorSuggestions.innerHTML = "<h3>Suggested Doctors:</h3>";

        doctors.forEach(doc => {
            const div = document.createElement('div');
            div.innerHTML = `
                <p><b>${doc.name}</b> (${doc.specialization})</p>
                <button onclick="selectDoctor(${doc.id}, '${doc.name}')">Select</button>
                <hr>
            `;
            doctorSuggestions.appendChild(div);
        });
    });

    // 👇 Make function global
    window.selectDoctor = function(id, name) {
        selectedDoctorId = id;
        selectedDoctor.innerText = name;
        appointmentDetails.style.display = 'block';
    };

    // 📅 Book Appointment
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;

        const response = await fetch('/book-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doctor_id: selectedDoctorId,
                date: date,
                time: time
            })
        });

        const data = await response.json();

        alert(data.message);
    });

});