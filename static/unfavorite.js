$(document).ready(function() {
	console.log("Ready")
	$(".unfavorite-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/unfavorite", {'id': courseId}, function () {
			alert("You have removed this class from your favorites list!");
		});
	});
	$(".taken-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		var course_info = $("#" + courseId).html();
		// console.log(course_info);
		// var thatId = this.id;
		// console.log(thatId);
		$("#" + courseId).empty();
		$("#taken").append(course_info);
		$('*[data-course-id =' + courseId + ']').remove();
		// $(".data-course-id").remove();
		$("#add-here-" + courseId).append("<button type=\"button\" class=\"btn btn-danger btn-xs remove-course\" id=" + this.id + ">Remove</button><br><br>");
		$.post("/move_to_taken", {'id': courseId}, function () {
			alert("You have moved this class to your taken courses list!");
		});
	});
	$(".remove-course").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/remove_from_taken", {'id': courseId}, function () {
			alert("You have removed this class from your taken list!");
		});
	});
});