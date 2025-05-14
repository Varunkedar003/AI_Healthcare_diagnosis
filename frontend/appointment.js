document.addEventListener('DOMContentLoaded', () => {
    const appointmentForm = document.getElementById('appointmentForm');
    const doctorSuggestions = document.getElementById('doctorSuggestions');
    const appointmentDetails = document.getElementById('appointmentDetails');
    const selectedDoctor = document.getElementById('selectedDoctor');
    const bookingForm = document.getElementById('bookingForm');

    appointmentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const symptoms = document.getElementById('symptoms').value.split(',').map(s => s.trim());
        
        try {
            const response = await fetch('http://127.0.0.1:5000/suggest-doctors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch doctor suggestions');
            }

            const doctors = await response.json();
            displayDoctorSuggestions(doctors);
        } catch (error) {
            console.error('Error:', error);
            doctorSuggestions.innerHTML = '<p>Error fetching doctor suggestions. Please try again.</p>';
        }
    });

    function displayDoctorSuggestions(doctors) {
        doctorSuggestions.innerHTML = '<h3>Suggested Doctors:</h3>';
        const ul = document.createElement('ul');
        doctors.forEach(doctor => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>${doctor.name}</strong> - ${doctor.specialization}
                <button class="select-doctor" data-id="${doctor.id}" data-name="${doctor.name}">Select</button>
            `;
            ul.appendChild(li);
        });
        doctorSuggestions.appendChild(ul);

        // Add event listeners to the select buttons
        document.querySelectorAll('.select-doctor').forEach(button => {
            button.addEventListener('click', (e) => {
                const doctorName = e.target.getAttribute('data-name');
                selectedDoctor.textContent = doctorName;
                appointmentDetails.style.display = 'block';
            });
        });
    }

    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        alert(`Appointment booked with ${selectedDoctor.textContent} on ${date} at ${time}`);
        // Here you would typically send this data to your backend
    });
});

