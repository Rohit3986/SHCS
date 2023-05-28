const sugarLevelForm = document.getElementById('sugarLevelForm');
const historyBody = document.getElementById('historyBody');

// Event listener for form submission
sugarLevelForm.addEventListener('submit', function(event) {
event.preventDefault();

// Retrieve form values
const date = document.getElementById('date').value;
const time = document.getElementById('time').value;
const level = parseInt(document.getElementById('level').value);

// Create sugar level object
const sugarLevel = { date, time, level };

// Save sugar level to local storage
saveSugarLevel(sugarLevel);

// Clear form inputs
sugarLevelForm.reset();

// Update table
updateSugarLevelTable();
});

// Function to save sugar level to local storage
function saveSugarLevel(sugarLevel) {
let sugarLevelHistory = JSON.parse(localStorage.getItem('sugarLevelHistory'));

if (!sugarLevelHistory) {
sugarLevelHistory = [];
}

sugarLevelHistory.push(sugarLevel);
localStorage.setItem('sugarLevelHistory', JSON.stringify(sugarLevelHistory));
}

// Function to update the sugar level table
function updateSugarLevelTable() {
historyBody.innerHTML = '';

const sugarLevelHistory = JSON.parse(localStorage.getItem('sugarLevelHistory'));

if (sugarLevelHistory) {
sugarLevelHistory.forEach(function(sugarLevel) {
const row = document.createElement('tr');
row.innerHTML = `
<td>${sugarLevel.date}</td>
<td>${sugarLevel.time}</td>
<td>${sugarLevel.level}</td>
`;
historyBody.appendChild(row);
});
}
}

// Initialize the table on page load
updateSugarLevelTable();
