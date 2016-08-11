from sqlalchemy import func
from model import Course, Partner, CoursePartner

from model import connect_to_db, db
from server import app

import requests

COURSERA_URL = "https://api.coursera.org/api/courses.v1?fields=primaryLanguages,subtitleLanguages,certificates,description,startDate,workload,domainTypes,photoUrl,partnerIds"

# COURSERA_URL_NEXT = "https://api.coursera.org/api/courses.v1?start={}&fields=primaryLanguages,certificates,description,startDate,workload,domainTypes"

COURSERA_PARTNERS_URL = "https://api.coursera.org/api/partners.v1"

UDEMY_URL = "https://www.udemy.com/api-2.0/courses?page_size=100"


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

    Course.query.delete()

    coursera_response = requests.get(COURSERA_URL)

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
        for category in categories:
            category = category.get('domainId', '<unknown>')
            subcategory = category.get('subdomainId', '<unknown>')]

        picture = element.get('photoUrl', '<unknown>')

        source = "Coursera"

        course = Course(title=title, type_course=type_course, description=description, url=url,
                        languages=languages, subtitles=subtitles, workload=workload, 
                        has_certificates=has_certificates, category=category, subcategory=subcategory,
                        picture=picture, source=source)

        for partner_id in partner_ids:
            try:
                partner = Partner.query.filter_by(partner_id=partner_id).one()
            except:
                pass


            course.partners.append(partner)

        db.session.add(course)

    db.session.commit()


# def load_udemy_courses():
#     """Load courses from Coursera API responses into database."""

#     udemy_response = requests.get(UDEMY_URL, auth=($UDEMY_CLIENT_ID, $UDEMY_CLIENT_SECRET))

#     udict = udemy_response.json()

#     results = udict['results']

#     for result in results:
#         title = result.get('title', '<unknown>')
#         url_end = result.get('url', '<unknown>')
#         if url_end != '<unknown>':
#             url = "https://www.udemy.com"
#         is_paid = result.get('is_paid', '<unknown>')
#         price = result.get('price', '<unknown>')
#         picture = result.get('image')
#         instructors = result.get('visible_instructors', '<unknown>')
#         partner = instructors.get('title', '<unknown>')
#         source = "Udemy"

#         course = Course(title=title, type_course=type_course, description=description, url=url,
#                         languages=languages, subtitles=subtitles, workload=workload, 
#                         has_certificates=has_certificates, categories=categories, picture=picture, source=source)

#         db.session.add(course)

#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_coursera_partners()
    load_coursera_courses()
    # load_udemy_courses()


    