import unittest
import os
import datetime

from testconfig import config
from wunderpy import Wunderlist
from wunderpy import api


try:
    EMAIL = config["login"]["email"]
    PASSWORD = config["login"]["password"]
    CLIENT_ID = config["login"]["client_id"]
except:  # no config, so travis is running
    EMAIL = os.environ.get("WUNDERPY_EMAIL")
    PASSWORD = os.environ.get("WUNDERPY_PASSWORD")
    CLIENT_ID = os.environ.get("WUNDERPY_CLIENT_ID")

if not EMAIL and not PASSWORD:
    __test__ = False
else:
    __test__ = True


class TestAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.wunderlist = Wunderlist(CLIENT_ID)
        cls.wunderlist.login(EMAIL, PASSWORD)


class TestBasicRequests(TestAPI):
    def test_login(self):
        try:
            self.wunderlist.login(EMAIL, PASSWORD)
        except:
            self.fail("Login failure")

    def test_me(self):
        '''Test some of the more trivial /me/* requests.'''
        # we're testing them in a batch because it's faster
        # and send_request is already tested in test_login

        me = api.calls.me()
        shares = api.calls.get_shares()
        services = api.calls.get_services()
        events = api.calls.get_events()
        settings = api.calls.get_settings()
        friends = api.calls.get_friends()

        try:
            results = self.wunderlist.send_requests([me, shares, services,
                                                    events, settings,
                                                    friends])
        except:
            self.fail("Batch request failure")

        me_result, shares_result, services_resukt, events_result, \
            settings_result, friends_result = results

        # more stupid assertions, just to make sure we have some valid result
        self.assertEqual(self.wunderlist.id, me_result["id"])
        self.assertIn("background", settings_result)
        # not sure what's going on with services and events, so i won't check
        self.assertIn("background", settings_result)
        self.assertEqual(type(friends_result), list)  # can't do much more


class TestTasks(TestAPI):
    def test_get_tasks(self):
        result = self.wunderlist.send_request(api.calls.add_task("test",
                                                                 "inbox"))
        task_id = result["id"]
        tasks = self.wunderlist.send_request(api.calls.get_all_tasks())
        self.assertFalse(len(result) < 1)  # make sure we have one task
        self.wunderlist.send_request(api.calls.delete_task(task_id))

    def test_add_task(self):
        due = datetime.date(2012, 12, 21).isoformat()
        add_task = api.calls.add_task("test", "inbox", due_date=due,
                                      starred=True)

        result = self.wunderlist.send_request(add_task)
        task_id = result["id"]

        self.assertEqual(result["due_date"], due)
        self.assertEqual(result["title"], "test")
        self.assertEqual(result["starred"], True)

        self.wunderlist.send_request(api.calls.delete_task(task_id))

    def test_task_note(self):
        result = self.wunderlist.send_request(api.calls.add_task("test",
                                                                 "inbox"))
        task_id = result["id"]
        add_note = api.calls.set_note_for_task("note", task_id)
        result = self.wunderlist.send_request(add_note)

        self.assertEqual(result["note"], "note")

        self.wunderlist.send_request(api.calls.delete_task(task_id))

    def test_task_reminder(self):
        result = self.wunderlist.send_request(api.calls.add_task("test",
                                                                 "inbox"))
        task_id = result["id"]

        reminder_date = datetime.date(2012, 12, 22).isoformat()
        add_reminder = api.calls.set_reminder_for_task(task_id, reminder_date)
        self.wunderlist.send_request(add_reminder)
        self.wunderlist.send_request(api.calls.delete_task(task_id))

    def test_complete_task(self):
        result = self.wunderlist.send_request(api.calls.add_task("test",
                                                                 "inbox"))
        task_id = result["id"]
        complete_task = api.calls.complete_task(task_id)
        complete = self.wunderlist.send_request(complete_task)
        self.assertIsNotNone(complete["completed_at"])
        self.wunderlist.send_request(api.calls.delete_task(task_id))

    def test_comments(self):
        # add a task
        add_task = api.calls.add_task("comment test", "inbox")
        task_result = self.wunderlist.send_request(add_task)
        task_id = task_result["id"]
        # add a comment to the task
        add_comment = api.calls.add_comment("test", task_id)
        comment_result = self.wunderlist.send_request(add_comment)
        task_comments = self.wunderlist.send_request(
            api.calls.get_comments(task_id))
        # see if there's a comment with the title we gave
        self.assertEqual("test", task_comments[0]["text"])
        # cleanup
        delete = self.wunderlist.send_request(api.calls.delete_task(task_id))


class TestLists(TestAPI):
    def test_get_lists(self):
        add_list = api.calls.add_list("test list")
        result = self.wunderlist.send_request(add_list)
        list_id = result["id"]

        lists = self.wunderlist.send_request(api.calls.get_lists())
        self.assertFalse(len(lists) < 1)

        self.wunderlist.send_request(api.calls.delete_list(list_id))

    def test_add_list(self):
        add_list = api.calls.add_list("test list")
        result = self.wunderlist.send_request(add_list)
        list_id = result["id"]

        self.assertEqual(result["title"], "test list")
        self.wunderlist.send_request(api.calls.delete_list(list_id))
