from sqlalchemy import func
from model import Course

from model import connect_to_db, db
from server import app

import requests

COURSERA_URL = "https://api.coursera.org/api/courses.v1?fields=primaryLanguages,certificates,description,startDate,workload,domainTypes"

# COURSERA_URL_NEXT = "https://api.coursera.org/api/courses.v1?start={}&fields=primaryLanguages,certificates,description,startDate,workload,domainTypes"

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

        slug = element.get('slug', '<unknown>')
        url = "https://www.coursera.org/learn/" + slug

        languages = element.get('primaryLanguages', '<unknown>')
        languages =  ", ".join(languages)

        workload = element.get('workload', '<unknown>')
		
        if element['certificates']:
            has_certificates = True
        else:
            has_certificates = False
		
        categories = element.get('domainTypes', '<unknown>')
        for category in categories:
            categories = [category.get('domainId', '<unknown>'), category.get('subdomainId', '<unknown>')]
            categories = ", ".join(categories)

        source = "Coursera"

        course = Course(title=title, type_course=type_course, description=description, url=url,
                        languages=languages, workload=workload, has_certificates=has_certificates,
                        categories=categories, source=source)

        db.session.add(course)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_coursera_courses()