$("#filters").on('click', function(evt) { 
	evt.preventDefault(); 
	var formInputs = $("#filters-form").serialize();
	$.get("/search/filters.json", formInputs, function (course_dict) {
		$("#search-results").empty();
		if ($.isEmptyObject(course_dict) == false) {
			$("#search-results").append("<p>Your search has yielded <b>" + Object.keys(course_dict).length + "</b> results: </p>");
			for (var k in course_dict) {
				// $("#search-results").append("<ul>");
				// var list = $('<ul>').appendTo('#search-results')
				$("#search-results").append("<img src=" + course_dict[k]['picture'] + " height=\"75\" width=\"100\"><h3>" + course_dict[k]['title'] + "</h3>" + course_dict[k]['description']);
				if (course_dict[k]['workload']) {
					$("#search-results").append("<ul><li>" + course_dict[k]['workload'] + "</li>");
				};
				if (course_dict[k]['price'] !== 0) {
					$("#search-results").append("<li>$" + course_dict[k]['price'] + "</li><li><a href=" + course_dict[k]['url'] + ">Go to this course</a></li><button class =\"favorite-button\" type=\"button\" id=" + k + ">Favorite this course</button></ul><br><br>");
				} else {
					$("#search-results").append("<li>Free</li><li><a href=" + course_dict[k]['url'] + " target =\"_blank\">Go to this course</a></li><button class =\"favorite-button\" type=\"button\" id=" + k + ">Favorite this course</button></ul><br><br>");
				};
			};
					
		} else if ($.isEmptyObject(course_dict) == true) {
			$("#search-results").append("<p>Sorry, we couldn't find any courses that matched your description! Please adjust your filters or <a href=\"/\">try another search.</a></p>");
		};
	});
});
console.log("Test");
$(document).ready(function() {
	$(".favorite-button").on("click", function(evt) {
		console.log("Hello");
		evt.preventDefault();
		console.log("Hi");
		console.log(this.id);
		var random = [1, 2, 3];
		// debugger;
		$.post("/favorite", {'id': this.id}, function (data) {
			alert(data.alert);
		});
	});
	console.log("Another test");
});