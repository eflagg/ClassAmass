$("#extra-langs").hide()
$("#extra-unis").hide()

var favorite = function() {
	$(".favorite-button").on("click", function(evt) {
		$.post("/favorite", {'id': this.id}, function (data) {
			alert(data.alert);
		});
	});
}

var taken = function() {
	$(".taken-button").on("click", function(evt) {
		$.post("/taken", {'id': this.id}, function (data) {
			alert(data.alert);
		});
	});
}

var lang_toggle = function() {
	$("#show-lang").on("click", function() {
		$("#extra-langs").toggle();
		if ($("#show-lang").html() !== "Show More") { 
			$("#show-lang").html("Show More");
		} else {
			$("#show-lang").html("Show Less");
		};
	});
}

var uni_toggle = function() {
	$("#show-uni").on("click", function() {
		$("#extra-unis").toggle();
		if ($("#show-uni").html() !== "Show More") { 
			$("#show-uni").html("Show More");
		} else {
			$("#show-uni").html("Show Less");
		};
	});
}

$("#filters").on('click', function(evt) { 
	evt.preventDefault(); 
	var formInputs = $("#filters-form").serialize();
	$.get("/search/filters.json", formInputs, function (course_dict, phrase_dict) {
		$("#search-results").empty();
		if ($.isEmptyObject(course_dict) == false) {
			$("#search-results").append("<h3 id=\"result-number\">Your search for <strong>" + "PUT IN LATER" + "</strong> has yielded <b>" + Object.keys(course_dict).length + "</b> results: </h3>");
			for (var k in course_dict) {
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
			favorite();
			taken();
			lang_toggle();
			uni_toggle();	
		} else if ($.isEmptyObject(course_dict) == true) {
			$("#search-results").append("<p>Sorry, we couldn't find any courses that matched your description! Please adjust your filters or <a href=\"/\">try another search.</a></p>");
		};
	});
});

favorite();
taken();
lang_toggle();
uni_toggle();