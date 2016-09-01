$(document).ready(function() {
	$(".unfavorite-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/unfavorite", {'id': courseId}, function(data) {
			$("#unfav-msg").html("You have removed this class from your favorites list!");
			if (data.course_no[0] === 0) {
				$("#fav-heading").html("");
			};
		});
	});
	$(".taken-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		var course_info = $("#" + courseId).html();
		$("#" + courseId).empty();
		$("#taken").append(course_info);
		$('*[data-course-id =' + courseId + ']').remove();
		$("#add-here-" + courseId).append("<button type=\"button\" class=\"btn btn-danger btn-xs remove-course\" id=" + this.id + ">Remove</button><br><br>");
		$.post("/move_to_taken", {'id': courseId}, function(data) {
			$("#unfav-msg").html("You have moved this class to your taken courses list!");
			if (data.course_no[0] === 0) {
				$("#fav-heading").html("");
			};
		});
	});
	$(".remove-course").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/remove_from_taken", {'id': courseId}, function(data) {
			$("#untaken-msg").html("You have removed this class from your taken list!");
			if (data.course_no[0] === 0) {
				$("#taken-heading").html("");
			};
		});
	});
});