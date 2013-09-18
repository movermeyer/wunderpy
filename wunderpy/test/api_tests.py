import unittest
import os

from testconfig import config
from wunderpy import Wunderlist
from wunderpy._api import API
from wunderpy._api_requests import Request


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            email = config["login"]["email"]
            password = config["login"]["password"]
        except:  # no config, so travis is running
            email = os.environ.get("WUNDERPY_EMAIL")
            password = os.environ.get("WUNDERPY_PASSWORD")

        cls.wunderlist = Wunderlist(email, password)
        cls.api = API()
        # we aren't testing anything from the wunderlist class aside from login
        # so just login with the api class
        cls.user_info = cls.api.login(email, password)


class TestAPIRequests(TestAPI):
    def test_login(self):
        try:
            self.wunderlist.login()
        except:
            self.fail("Login failure")

    def test_batch(self):
        '''Test a simple request using /batch'''
        me = Request.me()

        try:
            batch_results = self.api.send_requests([me])
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
            results = self.api.send_requests([me, shares, services, events,
                                             settings, friends])
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

    def test_tasks(self):
        '''Test all task related functionality'''
        import datetime

        due = datetime.date(2012, 12, 21).isoformat()
        add_task = Request.add_task("test", "inbox", due_date=due,
                                    starred=True)

        # sending a request now, because we need the list's id
        try:
            result = self.api.send_request(add_task)
        except:
            self.fail()
        new_task_id = result["id"]

        self.assertEqual(result["due_date"], due)
        self.assertEqual(result["title"], "test")
        self.assertEqual(result["starred"], True)

        # test adding a note and a reminder date
        add_note = Request.set_note_for_task("note", new_task_id)
        reminder = datetime.date(2012, 12, 22).isoformat()
        add_reminder = Request.set_reminder_for_task(new_task_id, reminder)
        try:
            results = self.api.send_requests([add_note, add_reminder])
        except:
            self.fail()

        note_result = next(results)
        reminder_result = next(results)

        self.assertEqual(note_result["note"], "note")
        # test reminder date here

        # test getting tasks
        get_tasks = Request.get_all_tasks()
        try:
            result = self.api.send_request(get_tasks)
        except:
            self.fail()

        if len(result) < 1:
            self.fail("Received no tasks")
        if not any(t["title"] == "test" for t in result):
            self.fail("No test task found")

        # delete everything
        delete = Request.delete_task(new_task_id)
        try:
            self.api.send_request(delete)
        except:
            self.fail()

    def test_lists(self):
        '''Test list related stuff'''

        add_list = Request.add_list("test list")
        try:
            result = self.api.send_request(add_list)
        except:
            self.fail()

        list_id = result["id"]
        add_task = Request.add_task("test", list_id)
        try:
            result = self.api.send_request(add_task)
        except:
            self.fail()

        # check that the list exists and has a task in it
        get_lists = Request.get_lists()
        get_tasks = Request.get_all_tasks()
        try:
            results = self.api.send_requests([get_lists, get_tasks])
        except:
            self.fail()

        lists = next(results)
        tasks = next(results)

        if not any(l["title"] == "test list" for l in lists):
            self.fail()

        if not any(t["list_id"] == list_id for t in tasks):
            self.fail()

        task_id = result["id"]
        delete_task = Request.delete_task(task_id)
        delete_list = Request.delete_list(list_id)
        try:
            self.api.send_requests([delete_task, delete_list])
        except:
            self.fail()
