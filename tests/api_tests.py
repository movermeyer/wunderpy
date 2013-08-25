import unittest
from testconfig import config
from wunderpy import Wunderlist


class TestAuth(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		email = config["login"]["email"]
		password = config["login"]["password"]
		cls.wunderlist = Wunderlist(email, password)

	def test_login(self):
		try:
			self.wunderlist.login()
		except:
			self.fail("Login failure")
