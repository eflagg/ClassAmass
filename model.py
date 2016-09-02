from flask_sqlalchemy import SQLAlchemy
import dictalchemy

db = SQLAlchemy()

class Course(db.Model):
	"""Course model."""

	__tablename__ = "courses"

	course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String, nullable=False)
	category = db.Column(db.String(1000))
	subcategory = db.Column(db.String(1000))
	price = db.Column(db.Integer, default=0)
	course_type = db.Column(db.String, default="self")
	source = db.Column(db.String, nullable=False)
	description = db.Column(db.Text)
	headline = db.Column(db.String(5000))
	language = db.Column(db.String(100))
	subtitles = db.Column(db.String(100))
	workload = db.Column(db.String(200))
	has_certificates = db.Column(db.Boolean, default=False)
	url = db.Column(db.String(500))
	picture = db.Column(db.String(500))

	def __repr__(self):
		return "<Course id=%s, title=%s>" % (self.course_id, self.title)


class Partner(db.Model):
	"""Partner mode."""

	__tablename__ = "partners"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	partner_id = db.Column(db.String(10), nullable=False, unique=True)
	name = db.Column(db.String(400), nullable=False)

	courses = db.relationship('Course', secondary="courses_partners", backref='partners')

	def __repr__(self):
		return "<Partner id=%s, name=%s>" % (self.partner_id, self.name)


class CoursePartner(db.Model):
	"""Association table for Course and Partner models."""

	__tablename__ = "courses_partners"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	partner_id = db.Column(db.String(10), db.ForeignKey('partners.partner_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<partner_id=%s, course_id=%s>" % (self.partner_id, self.course_id)


class User(db.Model):
	"""Table for User models."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	fname = db.Column(db.String(20), nullable=False)
	lname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.Text, nullable=False)

	courses_favorited = db.relationship('Course_Favorited', backref='users')
	courses_taken = db.relationship('Course_Taken', backref='users')
	courses_taking = db.relationship('Course_Taking', backref='users')
	ratings = db.relationship('Rating', backref='users')

	def __repr__(self):
		return "<User id=%s, fname=%s, lname=%s>" % (self.user_id, self.fname, self.lname)


class Course_Favorited(db.Model):
	"""Table for Courses favotited by Users."""

	__tablename__ = "courses_favorited"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Favorite user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Course_Taken(db.Model):
	"""Table for Courses taken by Users."""

	__tablename__ = "courses_taken"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Taken user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Course_Taking(db.Model):
	"""Table for Courses currently being taken by Users."""

	__tablename__ = "courses_taking"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Taking user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Rating(db.Model):
	"""Table for Ratings of Courses made by Users."""

	__tablename__ = "courses_ratings"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "<user_id=%s, course_id=%s, rating=%s>" % (self.user_id, self.course_id, self.rating)


dictalchemy.utils.make_class_dictable(Course)
dictalchemy.utils.make_class_dictable(Partner)
dictalchemy.utils.make_class_dictable(CoursePartner)
dictalchemy.utils.make_class_dictable(User)
dictalchemy.utils.make_class_dictable(Course_Favorited)
dictalchemy.utils.make_class_dictable(Course_Taken)
dictalchemy.utils.make_class_dictable(Course_Taking)
dictalchemy.utils.make_class_dictable(Rating)


def example_data():
	"""Fake sample data to test database queries."""

	bio_course = Course(course_id=1, title="Advanced Biology", course_type="self",
					 description="A course about advanced biology topics", 
					 url="www.course.com", language="en", 
					 subtitles=["fr", "zh"], workload="10 weeks, 2hr/week", 
					has_certificates=True, category="science", 
					subcategory="biology", picture="www.picture.com", 
					source="Coursera")
	art_hist_course = Course(course_id=2, title="Intro to Art History", course_type="instructor",
					 description="A course about European art history", 
					 url="www.course2.com", language="fr", 
					 subtitles=["en", "zh"], workload="52 lectures", 
					has_certificates=False, category="history", 
					subcategory="art history", picture="www.picture2.com", 
					source="Udemy")

	user = User(user_id="1", fname="Jane", lname="Doe", 
				email="jane@email.com",	password="pass")

	course_favorited = Course_Favorited(id="1", user_id="1", course_id="1")

	course_taken = Course_Taken(id="1", user_id="1", course_id="2")

	db.session.add_all([bio_course, art_hist_course, user, course_favorited, course_taken])
	db.session.commit()


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri='postgres:///courses'):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."