from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
	"""Course model."""

	__tablename__ = "courses"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	category = db.Column(db.String(100))
	subcategory = db.Column(db.String(100))
	is_free = db.Column(db.Boolean, default=True)
	price = db.Column(db.Integer)
	type_course = db.Column(db.String)
	level = db.Column(db.String)
	source = db.Column(db.String)
	description = db.Column(db.String(1000))
	languages = db.Column(db.String(5))
	workload = db.Column(db.String(200))
	# certificates = db.Column(String)

	def __repr__(self):
		return "<Course id=%s, title=%s>" % (self.id, self.title)


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

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