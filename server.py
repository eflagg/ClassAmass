from flask import Flask, render_template, request, session

import requests
from model import connect_to_db, db, Course

app = Flask(__name__)

app.secret_key = "SECRET"

COURSERA_URL = "https://api.coursera.org/api/courses.v1"


@app.route("/")
def index_page():
    """Show an homepage/inital search page."""

    return render_template("index.html")


@app.route("/search")
def show_search_results():
    """Show search results based on user input parameters."""

    phrase = request.args.get("search-phrase")

    try:
        relevent_courses = db.session.query(Course).filter(Course.title.like('%' + phrase + '%')).all()
        session['search-phrase'] = phrase

    except UnicodeEncodeError:
        pass

    return render_template("search.html", courses=relevent_courses)


@app.route("/search/filters")
def filter_results_by_price():
    """ Filter resuts based on user input parameters."""

    q = db.session.query(Course)
    phrase = session['search-phrase']

    price = request.args.get("price")
    languages = request.args.get("languages")
    # course_type = request.args.get("classtype")
    # certificates = request.args.get("certificates")
    
    phrase_arg = Course.title.like('%' + phrase + '%')

    if price:
        price_arg = Course.price <= price
    else:
        price_arg = ""

    if languages:
        language_arg = Course.languages.like('%' + languages + '%')
    else:
        language_arg = ""

    # if course_type:
    #     type_arg = Course.languages.like('%' + languages + '%')
    # else:
    #     language_arg = ""

    # if certificates:
    #     certificate_arg = Course.has_certificates = True
    # else:
    #     language_arg = ""

    args = (phrase_arg, price_arg, language_arg)

    query = q.filter(*args)
    print query

    try:
        relevent_courses = query.all()
    except UnicodeEncodeError:
        pass

    return render_template("search.html", courses=relevent_courses)


# @app.route("/search/filters")
# def filter_results_by_language():
#     """ Filter resuts based on user input parameters."""




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