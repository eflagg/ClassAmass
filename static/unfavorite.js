$(document).ready(function() {
	console.log("Ready")
	$(".unfavorite-button").on("click", function(evt) {
		$("#course-" + this.id).empty();
		$.post("/unfavorite", {'id': this.id}, function () {
			alert("You have removed this class from your favorites list!");
		});
	});
	$(".taken-button").on("click", function(evt) {
		var course_info = $("#course-" + this.id).html();
		console.log(course_info);
		$("#course-" + this.id).empty();
		$("#taken").append(course_info);
		$.post("/move_to_taken", {'id': this.id}, function () {
			alert("You have moved this class to your taken courses list!");
		});
	});
});