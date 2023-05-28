// Function to display a pop-up message
function showMessage(message) {
    alert(message);
  }
  
  // Function to cancel a specific meeting
  function cancelMeeting(event) {
    var timeSlot = event.target.parentNode;
    var timeRange = timeSlot.querySelector('span').textContent;
    showMessage('Your meeting has been cancelled for ' + timeRange);
  
    // Mark the time slot as cancelled
    timeSlot.classList.add('cancelled');
  
    // Save the updated list of cancelled meetings in localStorage
    saveCancelledMeetings();
  }
  
  // Function to cancel all meetings for a day
  function cancelAllMeetings(event) {
    var container = event.target.closest('.container');
    var date = container.querySelector('.date').textContent;
    showMessage('All meetings for ' + date + ' have been cancelled');
  
    // Remove the container from the page
    container.remove();
  
    // Save the updated list of cancelled meetings in localStorage
    saveCancelledMeetings();
  }
  
  // Function to save the list of cancelled meetings in localStorage
  function saveCancelledMeetings() {
    var cancelledMeetings = {};
  
    // Iterate through containers and time slots
    var containers = document.getElementsByClassName('container');
    for (var j = 0; j < containers.length; j++) {
      var container = containers[j];
      var date = container.querySelector('.date').textContent;
      var timeSlots = container.querySelectorAll('.time-slot');
  
      // Check if there are any cancelled meetings for the current date
      var cancelledTimeSlots = [];
      for (var k = 0; k < timeSlots.length; k++) {
        var timeSlot = timeSlots[k];
        var timeRange = timeSlot.querySelector('span').textContent;
  
        if (timeSlot.classList.contains('cancelled')) {
          cancelledTimeSlots.push(timeRange);
        }
      }
  
      if (cancelledTimeSlots.length > 0) {
        cancelledMeetings[date] = cancelledTimeSlots;
      }
    }
  
    // Save the updated list of cancelled meetings in localStorage
    localStorage.setItem('cancelledMeetings', JSON.stringify(cancelledMeetings));
  }
  
  // Attach event listeners to cancel buttons
  var cancelButtons = document.getElementsByClassName('cancel-button');
  for (var i = 0; i < cancelButtons.length; i++) {
    cancelButtons[i].addEventListener('click', cancelMeeting);
  }
  
  // Attach event listener to cancel all button
  var cancelAllButton = document.getElementById('cancel-all');
  cancelAllButton.addEventListener('click', cancelAllMeetings);
  
  // Retrieve cancelled meetings from localStorage
  var cancelledMeetings = JSON.parse(localStorage.getItem('cancelledMeetings')) || {};
  
  // Iterate through containers and time slots to mark the cancelled ones
  var containers = document.getElementsByClassName('container');
  for (var j = 0; j < containers.length; j++) {
    var container = containers[j];
    var date = container.querySelector('.date').textContent;
    var timeSlots = container.querySelectorAll('.time-slot');
  
    // Check if there are any cancelled meetings for the current date
    if (cancelledMeetings[date]) {
      var cancelledTimeSlots = cancelledMeetings[date];
  
      // Iterate through time slots and mark the cancelled ones
      for (var k = 0; k < timeSlots.length; k++) {
        var timeSlot = timeSlots[k];
        var timeRange = timeSlot.querySelector('span').textContent;
  
        if (cancelledTimeSlots.includes(timeRange)) {
          timeSlot.remove();
        }
      }
    }
  }
  