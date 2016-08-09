from sqlalchemy import func
from model import Course

from model import connect_to_db, db
from server import app

import requests

COURSERA_URL = "https://api.coursera.org/api/courses.v1?fields=primaryLanguages,certificates,description,startDate,workload,domainTypes"


def load_coursera_courses():
    """Load courses from api responses into database."""

    print "Courses"

    Course.query.delete()

    r = requests.get(COURSERA_URL)

    rdict = r.json()

    elements = rdict['elements']

    for element in elements:
		title = element.get('name', '<unknown>')
		type_course = element.get('courseType', '<unknown>')
		description = element.get('description', '<unknown>')
		# languages = element.get('primaryLanguages', '<unknown>')
		workload = element.get('workload', '<unknown>')
		# certificates = element.get('certificates', None)
		# keywords = [element.get('domainTypes', None ['domainId'], element['domainTypes']['domainId']]
		source = "Coursera"

		course = Course(title=title, type_course=type_course, source=source,
						description=description, workload=workload)

		db.session.add(course)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_coursera_courses()