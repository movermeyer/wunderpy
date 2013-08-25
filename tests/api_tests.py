import unittest
from testconfig import config
from wunderpy import Wunderlist
from wunderpy._api import API, Request


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

class TestAPIRequests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		email = config["login"]["email"]
		password = config["login"]["password"]
		cls.api = API()
		cls.user_info = cls.api.login(email, password)

	def test_batch(self):
		'''Test a simple request using /batch'''
		me = Request.me()
		settings = Request.get_settings()
		lists = Request.get_lists()
		inbox = Request("GET", "/inbox/tasks", body=None)

		try:
			batch_results = self.api.send_requests(me, settings, lists, inbox)
		except:
			self.fail("Batch request failure")
		me_result = next(batch_results)
		settings_result = next(batch_results)
		lists_result = next(batch_results)
		inbox_result = next(batch_results)		

		# if we get a correct id value, everything probably worked on our end
		self.assertEqual(self.user_info["id"], me_result["id"])
		# just checking for an arbitrary key in the settings output
		self.assertIn("background", settings_result)
		# check that each list has a title, since that's kinda important data
		for list in lists_result:
			self.assertIn("title", list)
		# check that each task in the inbox list has a title
		for task in inbox_result:
			self.assertIn("title", task)
