function scheduleCall() {
	event.preventDefault(); // prevent form submission

	// get selected date and time
	let selectedDate = document.getElementById("date").value;
	let selectedTime = document.getElementById("time").value;

	// do something with the selected date and time
	console.log("Selected date: " + selectedDate);
	console.log("Selected time: " + selectedTime);

	// redirect to confirmation page
	window.location.href = "confirmation.html";
}
