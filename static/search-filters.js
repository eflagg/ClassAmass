$("#filters").on('click', function(evt) { 
			evt.preventDefault(); 
			var formInputs = $("#filters-form").serialize();
			console.log(formInputs);
			$.get("/search/filters.json", formInputs, function (course_dict) {
				console.log(course_dict);
				$("#search-results").empty();
				console.log($.isEmptyObject(course_dict));
				if ($.isEmptyObject(course_dict) == false) {
					for (var k in course_dict) {
						$("#search-results").append("<img src=" + course_dict[k]['picture'] + " height=\"75\" width=\"100\"><li>" + course_dict[k]['title'] + "</li><li>" + course_dict[k]['description'] + "</li>");
						if (course_dict[k]['workload']) {
							$("#search-results").append("<li>" + course_dict[k]['workload'] + "</li>");
						};
						if (course_dict[k]['price'] !== 0) {
							$("#search-results").append("<li>" + course_dict[k]['price'] + "</li><li><a href=" + course_dict[k]['url'] + ">Go to this course</a></li>");
						} else {
							$("#search-results").append("<li>Free</li><li><a href=" + course_dict[k]['url'] + ">Go to this course</a></li>");
						};
					};
				} else if ($.isEmptyObject(course_dict) == true) {
					console.log("Hey there test");
					$("#search-results").append("<p>Sorry, we couldn't find any courses that matched your description! Please adjust your filters or <a href=\"/\">try another search.</a></p>");
					};
			});
		});