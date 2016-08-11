from sqlalchemy import func
from model import Course

from model import connect_to_db, db
from server import app

import requests

def test_load():
	
	i = 0
	while i < 4:
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

    test_load()