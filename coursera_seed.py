from sqlalchemy import func
from model import Course, Partner, CoursePartner, connect_to_db, db
from server import app
import requests

COURSERA_PARTNERS_URL = "https://api.coursera.org/api/partners.v1"


def load_coursera_partners():
    """Load partners from Coursera API responses into database"""

    Partner.query.delete()

    partner_api_response = requests.get(COURSERA_PARTNERS_URL)

    partner_api_response = partner_api_response.json()

    partners = partner_api_response['elements']

    for partner in partners:
        partner_id = partner.get('id', '<unknown>')
        name = partner.get('name', '<unknown>')

        partner = Partner(partner_id=partner_id, name=name)

        db.session.add(partner)

    db.session.commit()


def load_coursera_courses():
    """Load courses from Coursera API responses into database."""

    print "Coursera courses"

    # Course.query.delete()

    i = 0
    while i < 20:
		num = str(i * 100)

		coursera_response = requests.get("https://api.coursera.org/api/courses.v1?start=" + num + "&fields=primaryLanguages,subtitleLanguages,certificates,description,startDate,workload,domainTypes,photoUrl,partnerIds")
		
		coursera_response = coursera_response.json()

		elements = coursera_response['elements']

		for element in elements:
			title = element.get('name', '<unknown>')
			type_course = element.get('courseType', '<unknown>')
			description = element.get('description', '<unknown>')

			slug = element.get('slug', '<unknown>')
			url = "https://www.coursera.org/learn/" + slug

			languages = element.get('primaryLanguages', '<unknown>')
			languages =  ", ".join(languages)

			subtitles = element.get('subtitleLanguages', '<unknown>')
			subtitles = ", ".join(subtitles)

			workload = element.get('workload', '<unknown>')

			if element['certificates']:
				has_certificates = True
			else:
				has_certificates = False

			categories = element.get('domainTypes', '<unknown>')
			for item in categories:
				category = item.get('domainId', '<unknown>')
				subcategory = item.get('subdomainId', '<unknown>')

			picture = element.get('photoUrl', '<unknown>')

			source = "Coursera"

			course = Course(title=title, type_course=type_course, description=description, url=url,
			languages=languages, subtitles=subtitles, workload=workload, 
			has_certificates=has_certificates, category=category, subcategory=subcategory,
			picture=picture, source=source)

			db.session.add(course)

		i = i + 1

		db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_coursera_partners()
    load_coursera_courses()