from flask import Flask, render_template, request, session, jsonify, flash, redirect, url_for
from model import connect_to_db, db, Course, CoursePartner, Partner, User, Course_Favorited, Course_Taken, Course_Taking
from flask_debugtoolbar import DebugToolbarExtension
from helpers import get_user_by_email, get_user_by_session, is_favorited, is_taken, is_enrolled
import hashlib
from sqlalchemy import func
import dictalchemy

app = Flask(__name__)

app.secret_key = "SECRET"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def index_page():
    """Show an homepage/inital search page."""

    return render_template("index.html")


def get_language_count(phrase, *args):

    university = session.get('university')
    if university:
        q = db.session.query(Course.language, 
                                func.count(Course.language)
                                ).join(CoursePartner).join(Partner)
        del session['university']
    else:
        q = db.session.query(Course.language, 
                                    func.count(Course.language))
    q = q.filter(*args).group_by(Course.language)
    lang_results = q.all()
    lang_counts = {'el': 0, 'en': 0, 'zh': 0, 'af': 0, 'vi': 0, 'it': 0, 
                'ar': 0, 'et': 0, 'az': 0, 'id': 0, 'es': 0, 'ru': 0, 
                'sr': 0, 'nl': 0, 'pt': 0, 'nb': 0, 'tr': 0, 'lv': 0, 
                'tl': 0, 'th': 0, 'ro': 0, 'pl': 0, 'ta': 0, 'fr': 0, 
                'bg': 0, 'ms': 0, 'hr': 0, 'de': 0, 'hu': 0, 'fa': 0, 
                'hi': 0, 'fi': 0, 'da': 0, 'ja': 0, 'he': 0, 'uz': 0, 
                'ko': 0, 'sv': 0, 'ur': 0, 'sk': 0, 'uk': 0, 'mr': 0}
    for lang, count in lang_results:
        lang_counts[lang] = count

    return lang_counts


def is_user():
    """Returns email if user logged into session. Otherwise, returns false."""

    return session.get("current_user")


@app.route("/search")
def show_search_results():
    """Show search results based on user input parameters."""

    phrase = request.args.get("search")
    args = [((Course.title.ilike('%' + phrase + '%')) | 
            (Course.category.ilike('%' + phrase + '%')) | 
            (Course.subcategory.ilike('%' + phrase + '%')))]
    args = tuple(args)

    try:
        q = db.session.query(Course).filter(*args)
        courses = q.all()
        lang_counts = get_language_count(phrase, *args)
        session['search-phrase'] = phrase
    except UnicodeEncodeError:
        pass

    return render_template("search.html", 
                            courses=courses, 
                            phrase=phrase, 
                            langs=lang_counts)


@app.route("/search/filters.json")
def filter_results():
    """ Filter resuts based on user input parameters."""

    price = request.args.get("price")
    languages = request.args.getlist("languages")
    course_type = request.args.get("coursetype")
    certificates = request.args.get("certificates")
    source = request.args.get("source")
    university = request.args.getlist("university")
    phrase = request.args.get("search-phrase", session['search-phrase'])

    q = db.session.query(Course, Course.course_id)

    args = [((Course.title.ilike('%' + phrase + '%')) | 
            (Course.category.ilike('%' + phrase + '%')) | 
            (Course.subcategory.ilike('%' + phrase + '%')))]

    if price:
        price_arg = Course.price <= price
        args.append(price_arg)
    else:
        price_arg = None

    if languages:
        language_arg = Course.language.in_(languages)
        args.append(language_arg)
    else:
        language_arg = None

    if course_type:
        type_arg = Course.course_type == course_type
        args.append(type_arg)        
    else:
        type_arg = None

    if certificates == "yes":
        certificate_arg = (Course.has_certificates == True)
        args.append(certificate_arg)
    else:
        certificate_arg = None

    if source:
        source_arg = Course.source == source
        args.append(source_arg)
    else:
        source_arg = None

    if university:
        q = db.session.query(Course, Course.course_id).join(CoursePartner
                                                            ).join(Partner)
        university_arg = Partner.partner_id.in_(university)
        args.insert(0, university_arg)
        session['university'] = university
    else:
        university_arg = None
    
    args = tuple(args)

    query = q.filter(*args)

    try:
        courses = query.all()
        lang_counts = get_language_count(phrase, *args)
    except UnicodeEncodeError:
        pass

    course_dict = {}
    for course, course_id in courses:
        course_dict[course_id] = dictalchemy.utils.asdict(course)

    results = {'courses': course_dict, 'lang_counts': lang_counts, 
                'phrase': phrase}

    return jsonify(results)


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
    password = hashlib.sha224(password).hexdigest()

    if get_user_by_email(email):
        flash("You already have an account. Please log in here.")
        # alert = "You already have an account. Please log in."
        return redirect("/login")
        # return jsonify({"alert": alert})

    else:
        user = User(fname=fname, lname=lname, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        session["current_user"] = user.email
        flash("You have successfully created an account. Welcome!")

        return render_template("user_profile.html", 
                            user=user)


@app.route("/login")
def show_login_form():
    """ Show login form to user."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process login of user to check if in database and then add them to 
        session if they are.
    """

    email = request.form.get("email")
    password = request.form.get("password")
    password = hashlib.sha224(password).hexdigest()

    user = get_user_by_email(email)
    if user:
        if user.password == password:
            session["current_user"] = user.email
            flash("You have successfully logged in.")
            return redirect("/profile")
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

    email = session.get("current_user")

    print '$$$', email

    if email:
        user = get_user_by_email(email)
        fav_courses = db.session.query(User.user_id,Course.title,Course.url,
                                        Course.picture,Course.course_id).join(
                                        Course_Favorited).join(Course).filter(
                                        User.user_id==user.user_id).all()
        taken_courses = db.session.query(User.user_id,Course.title,Course.url,
                                        Course.picture,Course.course_id).join(
                                        Course_Taken).join(Course).filter(
                                        User.user_id==user.user_id).all()
        enrolled_courses = db.session.query(User.user_id,Course.title,Course.url,
                                        Course.picture,Course.course_id).join(
                                        Course_Taking).join(Course).filter(
                                        User.user_id==user.user_id).all()

        return render_template("user_profile.html", 
                                user=user, 
                                fav_courses=fav_courses, 
                                taken_courses=taken_courses,
                                enrolled_courses=enrolled_courses)
    if not email:
        flash("You must be logged in to see your profile page.")
        return redirect("/")


@app.route("/bookmark", methods=["POST"])
def favorite_course():
    """Add favorited course of user to courses_favorited table."""

    if is_user(): 
        email = session.get("current_user")
        user = get_user_by_email(email)
        course_id = request.form.get("id")

        if is_favorited(user, course_id):
            alert = "You have already added this course to your \
                    favorites list!"
        elif is_taken(user, course_id):
            alert = "You have already added this course to your \
                    courses taken list!"
        elif is_enrolled(user, course_id):
            alert = "You are currently enrolled in this course!"

        else:
            action = request.form.get("action")
            if action == "favorite":
                new_course = Course_Favorited(user_id=user.user_id, 
                                                course_id=course_id)
                alert = "You have successfully added this course to your favorites!"
            elif action == "enrolled":
                new_course = Course_Taking(user_id=user.user_id, 
                                                course_id=course_id)
                alert = "You have successfully added this course to your enrolled courses list!"
            elif action == "taken":
                new_course = Course_Taken(user_id=user.user_id, 
                                                course_id=course_id)
                alert = "You have successfully added this course to your taken courses list!"
            db.session.add(new_course)
            db.session.commit()
    else:
        alert = "You must be signed in to add this course."

    return jsonify({'alert': alert})


@app.route("/unfavorite", methods=["POST"])
def unfavorite_course():
    """Remove favorited course of user from courses_favorited table."""

    course_id = request.form.get("id")
    email = session.get("current_user")
    user = get_user_by_email(email)
    course = Course_Favorited.query.filter_by(user_id=user.user_id, 
                                                course_id=course_id).first()
    db.session.delete(course)
    db.session.commit()

    num_courses = db.session.query(func.count("*")).select_from(Course_Favorited
                                    ).filter_by(user_id=user.user_id).one()

    return jsonify({"course_no": num_courses})


@app.route("/move_to_taken", methods=["POST"])
def move_course_from_fav_to_taken_list():
    """Move favorited course of user from courses_favorited table to 
        courses_taken table.
    """

    course_id = request.form.get("id")
    email = session.get("current_user")
    user = get_user_by_email(email)
    fav_course = Course_Favorited.query.filter_by(user_id=user.user_id, 
                                                course_id=course_id).first()
    db.session.delete(fav_course)
    taken_course = Course_Taken(user_id=user.user_id, course_id=course_id)
    db.session.add(taken_course)
    db.session.commit()

    num_courses = db.session.query(func.count("*")).select_from(Course_Favorited
                                    ).filter_by(user_id=user.user_id).one()

    return jsonify({"course_no": num_courses})


@app.route("/remove_from_taken", methods=["POST"])
def remove_taken_course():
    """Remove taken course of user from courses_taken table."""

    course_id = request.form.get("id")
    email = session.get("current_user")
    user = get_user_by_email(email)
    course = Course_Taken.query.filter_by(user_id=user.user_id, 
                                            course_id=course_id).first()
    db.session.delete(course)
    db.session.commit()

    num_courses = db.session.query(func.count("*")).select_from(Course_Taken
                                    ).filter_by(user_id=user.user_id).one()

    return jsonify({"course_no": num_courses})


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")