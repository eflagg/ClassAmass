$(document).ready(function() {
	console.log("Ready")
	$(".unfavorite-button").on("click", function(evt) {
		console.log(this);
		// $(this).html("");
		// console.log("Hello");
		// evt.preventDefault();
		// console.log("Hi");
		console.log(this.id);
		$("#course-" + this.id).empty();
		// var random = [1, 2, 3];
		// debugger;
		$.post("/unfavorite", {'id': this.id}, function () {
			alert("You have removed this class from your favorites list!");
		});
	});
	// console.log("Another test");
});