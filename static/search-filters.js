$("#extra-langs").hide()
$("#extra-unis").hide()

var favorite = function() {
	$(".favorite-button").on("click", function(evt) {
		var thatId = this.id;
		console.log(thatId);
		$.post("/bookmark", {'id': this.id, 'action': 'favorite'}, function(data) {
			console.log(data.alert);
			$("#btn-response-msg-" + thatId).html(data.alert);
		});
	});
}

var taken = function() {
	$(".taken-button").on("click", function(evt) {
		var thatId = this.id;
		console.log(thatId);
		$.post("/bookmark", {'id': this.id, 'action': 'taken'}, function(data) {
			$("#btn-response-msg-" + thatId).html(data.alert);
		});
	});
}

var enrolled = function() {
	$(".enrolled-button").on("click", function(evt) {
		console.log("clicked");
		var thatId = this.id;
		console.log(thatId);
		$.post("/bookmark", {'id': this.id, 'action': 'enrolled'}, function(data) {
			console.log(data.alert);
			$("#btn-response-msg-" + thatId).html(data.alert);
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
	$.get("/search/filters.json", formInputs, function(results) {
		$("#main-search-div").empty();
		var course_dict = results['courses'];
		if ($.isEmptyObject(course_dict) == false) {
			$("#main-search-div").append("<div id=\"search-results\"><h3 id=\"result-number\">Your search for <strong>" + results["phrase"] + "</strong> has yielded <b>" + Object.keys(course_dict).length + "</b> results: </h3>");
			for (var k in course_dict) {
				if (course_dict[k]['workload'] && (course_dict[k]['price'] !== 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Workload: " + course_dict[k]['workload'] + "<br>Price: $" + course_dict[k]['price'] + "</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button> <button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button> <button class=\"btn btn-success enrolled-button btn-xs\" id=" + k + ">Enrolled</button><p id=\"btn-response-msg-" + k + "\"></p></div></div>");
				} else if (course_dict[k]['workload'] && (course_dict[k]['price'] === 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Workload: " + course_dict[k]['workload'] + "<br>Price: Free</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button> <button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button> <button class=\"btn btn-success enrolled-button btn-xs\" id=" + k + ">Enrolled</button><p id=\"btn-response-msg-" + k + "\"></p></div></div>");
				} else if (!(course_dict[k]['workload']) && (course_dict[k]['price'] !== 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Price: $" + course_dict[k]['price'] + "</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button> <button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button> <button class=\"btn btn-success enrolled-button btn-xs\" id=" + k + ">Enrolled</button><p id=\"btn-response-msg-" + k + "\"></p></div></div>");
				} else if (!(course_dict[k]['workload']) && (course_dict[k]['price'] === 0)) {
					$("#main-search-div").append("<div class=\"media well\"><div class=\"media-left media-middle\"><a href=" + course_dict[k]['url'] + " target =\"_blank\"><img class=\"media-object\" src=" + course_dict[k]['picture'] + " alt=\"course pic\"></a></div><div class=\"media-body\"><h4 class=\"media-heading\">" + course_dict[k]['title'] + "</h4><p>" + course_dict[k]['description'].slice(0,350) + "</p><p>Price: Free</p><button class =\"btn btn-danger favorite-button btn-xs\" type=\"button\" id=" + k + ">Favorite</button> <button class=\"btn btn-success taken-button btn-xs\" id=" + k + ">Taken</button> <button class=\"btn btn-success enrolled-button btn-xs\" id=" + k + ">Enrolled</button><p id=\"btn-response-msg-" + k + "\"></p></div></div>");
				};
				$("#main-search-div").append("<p id=\"btn-response-msg-" + k + "></p>");
			};
			for (var l in results["lang_counts"]) {
				$("#" + l).html(results["lang_counts"][l]);
			};
			favorite();
			taken();
			enrolled();
		} else if ($.isEmptyObject(course_dict) == true) {
			$("#main-search-div").append("<p>Sorry, we couldn't find any courses that matched your description! Please adjust your filters or <a href=\"/\">try another search.</a></p>");
		};
	});
});

favorite();
taken();
enrolled();
lang_toggle();
uni_toggle();