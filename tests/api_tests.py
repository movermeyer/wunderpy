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
		me = Request.me()
		settings = Request.get_settings()
		lists = Request.get_lists()
		inbox = Request("GET", "/inbox/tasks", body=None)

		batch_results = self.api.queue_requests(me, settings, lists, inbox)
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
		# check taht each task in the inbox list has a title
		for task in inbox_result:
			self.assertIn("title", task)
