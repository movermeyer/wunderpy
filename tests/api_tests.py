import unittest
from testconfig import config
from wunderpy import Wunderlist


class TestAPI(unittest.TestCase):
	def setUp(self):
		email = config["login"]["email"]
		password = config["login"]["password"]
		self.wunderlist = Wunderlist(email, password)
		self._api = self.wunderlist._api

	def test_login(self):
		try:
			self.wunderlist.login()
		except:
			self.fail("Login failure")
