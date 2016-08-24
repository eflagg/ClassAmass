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
		$("#main-search-div").empty();
		if ($.isEmptyObject(course_dict) == false) {
			$("#main-search-div").append("<div id=\"search-results\"><h3 id=\"result-number\">Your search for <strong>" + "PUT IN LATER" + "</strong> has yielded <b>" + Object.keys(course_dict).length + "</b> results: </h3>");
			for (var k in course_dict) {
				if (course_dict[k]['workload'] && (course_dict[k]['price'] !== 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Workload: " + course_dict[k]['workload'] + "<br>Price: $" + course_dict[k]['price'] + "</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button><button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button></div></div></div>");
				} else if (course_dict[k]['workload'] && (course_dict[k]['price'] === 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Workload: " + course_dict[k]['workload'] + "<br>Price: Free</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button><button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button></div></div></div>");
				} else if (!(course_dict[k]['workload']) && (course_dict[k]['price'] !== 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Price: $" + course_dict[k]['price'] + "</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button><button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button></div></div></div>");
				} else if (!(course_dict[k]['workload']) && (course_dict[k]['price'] === 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Price: Free</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button><button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button></div></div></div>");
				};
			}; 
			favorite();
			taken();
			lang_toggle();
			uni_toggle();	
		} else if ($.isEmptyObject(course_dict) == true) {
			$("#main-search-div").append("<p>Sorry, we couldn't find any courses that matched your description! Please adjust your filters or <a href=\"/\">try another search.</a></p>");
		};
	});
});

favorite();
taken();
lang_toggle();
uni_toggle();