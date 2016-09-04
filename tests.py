from server import app, get_language_count
import unittest
from model import db, connect_to_db, Course, example_data
from helpers import get_user_by_email, get_user_by_session, is_favorited, is_taken, is_enrolled

class FlaskTests(unittest.TestCase):

	def setUp(self):
		"""Set up by creating fake client."""

		self.client = app.test_client()
		app.config['TESTING'] = True
		# app.config['SECRET_KEY'] = 'key'

	def test_index(self):
		"""Test for main search page."""

		client = app.test_client()
		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn("<h1>What do you want to learn about?</h1>", result.data)


	def test_register_form(self):
		"""Test for registration page."""

		client = app.test_client()
		result = self.client.get("/register")
		self.assertEqual(result.status_code, 200)
		self.assertIn("<h3>Sign up now!</h3>", result.data)


	def test_login_form(self):
		"""Test for registration page."""

		client = app.test_client()
		result = self.client.get("/login")
		self.assertEqual(result.status_code, 200)
		self.assertIn("<h3>Log in!</h3>", result.data)


class FlaskDBTests(unittest.TestCase):
	"""Tests querying and changing database."""

	def setUp(self):
		"""Set up by creating testdb and fake client."""

		self.client = app.test_client()
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		connect_to_db(app, "postgresql:///testdb")

		with self.client as c:
			with c.session_transaction() as session:
				session['current_user'] = "jane@email.com"

		db.create_all()
		example_data()

	def tearDown(self):
		"""Tear down by droping testdb."""

		db.session.close()
		db.drop_all()


	def test_login(self):
		"""Test query to db to get user from input of email."""

		result = self.client.get("/profile", follow_redirects=True)
		self.assertIn("Jane", result.data)


	def test_user_by_email(self):

		jane = get_user_by_email("jane@email.com")

		assert jane.lname == "Doe"


	def test_user_by_session(self):

		jane = get_user_by_session()

		assert jane.lname == "Doe"


	def test_is_favorited(self):

		jane = get_user_by_email("jane@email.com")

		assert is_favorited(jane, 1) is True


	def test_is_taken(self):

		jane = get_user_by_email("jane@email.com")

		assert is_taken(jane, 2) is True


	def test_is_enrolled(self):

		jane = get_user_by_email("jane@email.com")

		assert is_enrolled(jane, 1) is False



		# assert get_user_by_email("jane@email.com"). "<User id=1, fname=Jane, lname=Doe>"


	# def test_logout(self):
	# 	"""Test for registration page."""

	# 	with self.client as c:
	# 		with c.session_transaction() as sess:
	# 			sess['current_user'] = test
	# 			result = self.client.get("/logout")
	# 			self.assertEqual(result.status_code, 200)
	# 			self.assertIn("You have successfully logged out.", result.data)

	# def test_search(self):
	# 	"""Test initial search results."""

	# 	client = app.test_client()
	# 	result = self.client.get("/search", data={'search': 'biology'})
	# 	self.assertEqual(result.status_code, 200)
	# 	self.assertIn(" ", result.data)


# class MyAppUnitTestCase(unittest.TestCase):
# 	"""Unit tests."""

#     def test_language_count():
#     	assert get_language_count('biology', )


if __name__ == '__main__':
    unittest.main()