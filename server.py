from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "SECRET"


@app.route("/")
def index_page():
    """Show an homepage/inital search page."""

    return render_template("index.html")


@app.route("/search_results")
def show_search_results():
	"""Show search results based on user input parameters."""

	return render_template("search_results.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")