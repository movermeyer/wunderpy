import unittest
from testconfig import config
from wunderpy import Wunderlist

class TestAuth(unittest.TestCase):
	def setUp(self):
		email = config["login"]["email"]
		password = config["login"]["password"]
		self.wunderlist = Wunderlist(email, password)

	def test_login(self):
		try:
			self.wunderlist.login()
		except Exception as e:
			self.fail("Login failure")
