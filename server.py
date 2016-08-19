from flask import Flask, render_template, request, session, jsonify, flash, redirect, url_for
from model import connect_to_db, db, Course, CoursePartner, Partner, User, Courses_Favorited
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "SECRET"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def index_page():
    """Show an homepage/inital search page."""

    return render_template("index.html")


@app.route("/search")
def show_search_results():
    """Show search results based on user input parameters."""

    phrase = request.args.get("search-phrase")

    try:
        q = db.session.query(Course).filter((Course.title.ilike('%' + phrase + '%')) | (Course.category.ilike('%' + phrase + '%')) | (Course.subcategory.ilike('%' + phrase + '%')))
        relevent_courses = q.all()
        session['search-phrase'] = phrase
    except UnicodeEncodeError:
        pass

    return render_template("search.html", courses=relevent_courses, phrase=phrase)


@app.route("/search/filters.json")
def filter_results_by_price():
    """ Filter resuts based on user input parameters."""

    # phrase = session['search-phrase']

    price = request.args.get("price")
    languages = request.args.getlist("languages")
    course_type = request.args.get("coursetype")
    certificates = request.args.get("certificates")
    source = request.args.get("source")
    university = request.args.getlist("university")
    phrase = request.args.get("search-phrase", session['search-phrase'])

    q = db.session.query(Course.course_id, Course.title, Course.description, Course.picture, Course.url, Course.workload, Course.price)

    args = [((Course.title.ilike('%' + phrase + '%')) | (Course.category.ilike('%' + phrase + '%')) | (Course.subcategory.ilike('%' + phrase + '%')))]

    if price:
        price_arg = Course.price <= price
        args.append(price_arg)
    else:
        price_arg = None

    if languages:
        language_arg = Course.languages.in_(languages)
        args.append(language_arg)
    else:
        language_arg = None

    if course_type == "self":
        type_arg = ((Course.course_type.like('%ondemand%')) | (Course.course_type == None))
        args.append(type_arg)
    elif course_type == "instructor":
        type_arg = Course.course_type.like('%session%')
        args.append(type_arg)
    else:
        type_arg = None

    if certificates == "yes":
        certificate_arg = (Course.has_certificates == True)
        args.append(certificate_arg)
    else:
        certificate_arg = None

    if source == "coursera":
        source_arg = (Course.source == "Coursera")
        args.append(source_arg)
    if source == "udemy":
        source_arg = (Course.source == "Udemy")
        args.append(source_arg)
    else:
        source_arg = None

    if university:
        q = db.session.query(Course.course_id, Course.title, Course.description, Course.picture, Course.url, Course.workload, Course.price).join(CoursePartner).join(Partner)
        university_arg = Partner.name.in_(university)
        args.insert(0, university_arg)
    else:
        university_arg = None
    
    args = tuple(args)

    query = q.filter(*args)

    try:
        courses = query.all()
    except UnicodeEncodeError:
        pass

    course_dict = {}
    for course_id, title, description, picture, url, workload, price in courses:
        course_dict[course_id] = {'title': title, 'description': description, 'picture': picture, 'price': price, 'url': url, 'workload': workload}

    return jsonify(course_dict)


@app.route("/register")
def show_register_form():
    """ Show register form to user."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def process_registeration():
    """Process regisration form and create new user in database"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    session["current_user"] = user.email
    flash("You have successfully created an account. Welcome!")

    return render_template("user_profile.html", user=user)


@app.route("/login")
def show_login_form():
    """ Show login form to user."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process login of user to check if in database and then add them to session if they are."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user != None:
        if user.password == password:
            session["current_user"] = user.email
            courses = db.session.query(User.user_id,Course.title,Course.url,Course.picture).join(Courses_Favorited).join(Course).filter(User.user_id==user.user_id).all()
            flash("You have successfully logged in.")
            return redirect(url_for("show_user_page", user=user, courses=courses))
        elif user.password != password:
            flash("Incorrect password.")
            return redirect("/login")
    elif user == None:
        flash("This email is not in our database.")
        return redirect("/login")


@app.route("/logout")
def process_logout():
    """Log user out of session."""

    del session["current_user"]
    flash("You have successfully logged out.")

    return redirect("/")


@app.route("/profile")
def show_user_page():
    """Show user profile page."""

    email = session["current_user"]
    user = User.query.filter_by(email=email).first()
    courses = db.session.query(User.user_id,Course.title,Course.url,Course.picture).join(Courses_Favorited).join(Course).filter(User.user_id==user.user_id).all()

    return render_template("user_profile.html", user=user, courses=courses)


@app.route("/favorite", methods=["POST"])
def favorite_course():
    """Add favorited course of user to courses_favorited table."""

    email = session.get("current_user")
    if email: 
        course_id = request.form.get("id")
        user = User.query.filter_by(email=email).one()
        favorite_course = Courses_Favorited(user_id=user.user_id, course_id=course_id)
        db.session.add(favorite_course)
        db.session.commit()
        alert = "You have successfully added this course to your favorites list!"
    if not email:
        print "Hi"
        alert = "You must be signed in to favorite a course!"
        
    return jsonify({'alert': alert})


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")