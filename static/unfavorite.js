$("#enrolled").hide();
$("#taken").hide();
$("#favorite").hide();

$(document).ready(function() {
	$(".unfavorite-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/unfavorite", {'id': courseId}, function(data) {
			$("#unfav-msg").html("You have removed this class from your favorites list!");
			$(function() {
				$("#unfav-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#favorite").html("<h4>You have no favorite courses.</h4>");
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
		$.post("/move_to_taken", {'id': courseId, 'origin': 'fav'}, function(data) {
			$("#unfav-msg").html("You have moved this class to your taken courses list!");
			$(function() {
				$("#unfav-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#favorite").html("<h4>You have no favorite courses.</h4>");
			};
		});
	});
	$(".enrolled-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		var course_info = $("#" + courseId).html();
		$("#" + courseId).empty();
		if ($("#enrolled").html().indexOf("You are currently not enrolled") !== -1) {
			console.log("index", $("#enrolled").html().indexOf("You have not completed"));
			$("#enrolled").html("");
		};
		$("#enrolled").append(course_info);
		$('*[data-course-id =' + courseId + ']').remove();
		$("#add-here-" + courseId).append("<button type=\"button\" class=\"btn btn-danger btn-xs unenroll\" id=" + this.id + ">Remove</button> <button type=\"button\" class=\"btn btn-danger btn-xs completed-button\" id=" + this.id + ">Completed</button><br><br>");
		$.post("/move_to_enrolled", {'id': courseId}, function(data) {
			$("#unfav-msg").html("You have moved this class to your currently enrolled list!");
			$(function() {
				$("#unfav-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#favorite").html("<h4>You have no favorite courses.</h4>");
			};
		});
	});
	$(".remove-course").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/remove_from_taken", {'id': courseId}, function(data) {
			$("#untaken-msg").html("You have removed this class from your taken list!");
			$(function() {
				$("#untaken-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#taken").html("<h4>You have not completed any courses.</h4>");
			};
		});
	});
	$(".completed-button").on("click", function(evt) {
		courseId = $(this).data("course-id");
		var course_info = $("#" + courseId).html();
		$("#" + courseId).empty();
		if ($("#taken").html().indexOf("You have not completed") !== -1) {
			console.log("index", $("#taken").html().indexOf("You have not completed"));
			$("#taken").html("");
		};
		$("#taken").append(course_info);
		$('*[data-course-id =' + courseId + ']').remove();
		$("#add-here-" + courseId).append("<button type=\"button\" class=\"btn btn-danger btn-xs remove-course\" id=" + this.id + ">Remove</button><br><br>");
		$.post("/move_to_taken", {'id': courseId, 'origin': 'enrolled'}, function(data) {
			$("#unenroll-msg").html("You have moved this class to your taken courses list!");
			$(function() {
				$("#unenroll-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#enrolled").html("<h4>You are not currently enrolled in any courses.</h4>");
			};
		});
	});
	$(".unenroll").on("click", function(evt) {
		courseId = $(this).data("course-id");
		$("#" + courseId).empty();
		$.post("/remove_from_enrolled", {'id': courseId}, function(data) {
			$("#unenroll-msg").html("You have removed this class from your currentlly enrolled list!");
			$(function() {
				$("#unenroll-msg").delay(2500).fadeOut();
			});
			if (data.course_no[0] === 0) {
				$("#enrolled").html("<h4>You are not currently enrolled in any courses.</h4>");
			};
		});
	});
	$(".class-heading").on("click", function() {
		$("#" + this.id.slice(0, -8)).toggle();
	});
});

// $(function() {
// 	$(".no-prof-courses-note").delay(2500).fadeOut();
// });