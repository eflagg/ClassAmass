from server import app, get_language_count
import unittest
from model import db, connect_to_db, Course, example_data

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


	def test_registry_form(self):
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
		"""Set up by creating fake client."""

		self.client = app.test_client()
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		connect_to_db(app, "postgresql:///testdb")

		db.create_all()
		example_data()



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