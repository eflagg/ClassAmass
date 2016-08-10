from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
	"""Course model."""

	__tablename__ = "courses"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	categories = db.Column(db.String(1000))
	# subcategory = db.Column(db.String(100))
	is_paid = db.Column(db.Boolean, default=False)
	price = db.Column(db.Integer)
	type_course = db.Column(db.String)
	dates = db.Column(db.DateTime)
	level = db.Column(db.String)
	source = db.Column(db.String)
	description = db.Column(db.String(5000))
	languages = db.Column(db.String(10))
	workload = db.Column(db.String(200))
	has_certificates = db.Column(db.Boolean, default=False)
	url = db.Column(db.String(500))
	picture = db.Column(db.String(500))

	def __repr__(self):
		return "<Course id=%s, title=%s>" % (self.id, self.title)


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///courses'
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