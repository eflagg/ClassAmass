from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
	"""Course model."""

	__tablename__ = "courses"

	course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String, nullable=False)
	category = db.Column(db.String(1000))
	subcategory = db.Column(db.String(100))
	is_paid = db.Column(db.Boolean, default=False)
	price = db.Column(db.Integer)
	type_course = db.Column(db.String)
	# dates = db.Column(db.DateTime)
	# level = db.Column(db.String)
	source = db.Column(db.String, nullable=False)
	description = db.Column(db.String(10000))
	languages = db.Column(db.String(50))
	subtitles = db.Column(db.String(50))
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


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///courses2'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."