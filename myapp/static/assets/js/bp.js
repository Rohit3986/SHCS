    // Function to save blood pressure to local storage
    function saveBloodPressure(bloodPressure) {
        let bloodPressureHistory = JSON.parse(localStorage.getItem('bloodPressureHistory'));
    
        if (!bloodPressureHistory) {
        bloodPressureHistory = [];
        }
    
        bloodPressureHistory.push(bloodPressure);
        localStorage.setItem('bloodPressureHistory', JSON.stringify(bloodPressureHistory));
        }
    
        // Function to update the blood pressure table
        function updateBloodPressureTable() {
        const historyBody = document.getElementById('historyBody');
        historyBody.innerHTML = '';
    
        const bloodPressureHistory = JSON.parse(localStorage.getItem('bloodPressureHistory'));
    
        if (bloodPressureHistory) {
        bloodPressureHistory.forEach(function(bloodPressure) {
            const row = document.createElement('tr');
            row.innerHTML = `
            <td>${bloodPressure.date}</td>
            <td>${bloodPressure.time}</td>
            <td>${bloodPressure.systolic}</td>
            <td>${bloodPressure.diastolic}</td>
            `;
            historyBody.appendChild(row);
        });
        }
        }
    
        // Event listener for form submission
        document.addEventListener('DOMContentLoaded', function() {
        const bloodPressureForm = document.getElementById('bloodPressureForm');
    
        bloodPressureForm.addEventListener('submit', function(event) {
        event.preventDefault();
    
        // Retrieve form values
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const systolic = parseInt(document.getElementById('systolic').value);
        const diastolic = parseInt(document.getElementById('diastolic').value);
    
        // Create blood pressure object
        const bloodPressure = { date, time, systolic, diastolic };
    
        // Save blood pressure to local storage
        saveBloodPressure(bloodPressure);
    
        // Clear form inputs
        bloodPressureForm.reset();
    
        // Update table
        updateBloodPressureTable();
        });
    
        // Initialize the table on page load
        updateBloodPressureTable();
        });