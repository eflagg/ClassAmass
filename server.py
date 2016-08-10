from flask import Flask, render_template, request

import requests
from model import connect_to_db, db, Course

app = Flask(__name__)

app.secret_key = "SECRET"

COURSERA_URL = "https://api.coursera.org/api/courses.v1"


@app.route("/")
def index_page():
    """Show an homepage/inital search page."""

    return render_template("index.html")


@app.route("/search-results")
def show_search_results():
    """Show search results based on user input parameters."""

    phrase = request.args.get("search-phrase")

    try:
        relevent_courses = db.session.query(Course).filter(Course.title.like('%' + phrase + '%')).all()

    except UnicodeEncodeError:
        pass


    # print relevent_courses

    return render_template("search_results.html", courses=relevent_courses)


# @app.route("/search-results")
# def show_search_results():
# 	"""Show search results based on user input parameters."""

# 	search_phrase = request.args.get("search-phrase")
# 	print search_phrase

# 	payload = {"q": "search", "query": search_phrase}

# 	response = requests.get(COURSERA_URL)

# 	# r = requests.get("https://api.coursera.org/api/courses.v1")

# 	rdict = response.json()

# 	elements = rdict['elements']

# 	return render_template("search_results.html", elements=elements)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")