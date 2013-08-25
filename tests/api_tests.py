import unittest
from testconfig import config
from wunderpy import Wunderlist
from wunderpy._api import API
from wunderpy._api_requests import Request


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

        try:
            batch_results = self.api.send_requests(me)
        except:
            self.fail("Batch request failure")
        me_result = next(batch_results)

        # if we get a correct id value, everything probably worked on our end
        self.assertEqual(self.user_info["id"], me_result["id"])

    def test_me(self):
        '''Test some of the more trivial /me/* requests.'''
        # we're testing them in a batch because it's faster
        # and send_request is already tested in test_login

        me = Request.me()
        shares = Request.get_shares()
        services = Request.get_services()
        events = Request.get_events()
        settings = Request.get_settings()
        friends = Request.get_friends()

        try:
            results = self.api.send_requests(me, shares, services, events,
                                             settings, friends)
        except:
            self.fail("Batch request failure")

        me_result = next(results)
        shares_result = next(results)
        services_result = next(results)
        events_result = next(results)
        settings_result = next(results)
        friends_result = next(results)

        # more stupid assertions, just to make sure we have some valid result
        self.assertEqual(self.user_info["id"], me_result["id"])
        self.assertIn("background", settings_result)
        # not sure what's going on with services and events, so i won't check
        self.assertIn("background", settings_result)
        self.assertEqual(type(friends_result), list)  # can't do much more
