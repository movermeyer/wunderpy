import unittest
import os

from testconfig import config
from wunderpy import Wunderlist
from wunderpy import api


try:
    EMAIL = config["login"]["email"]
    PASSWORD = config["login"]["password"]
except:  # no config, so travis is running
    EMAIL = os.environ.get("WUNDERPY_EMAIL")
    PASSWORD = os.environ.get("WUNDERPY_PASSWORD")


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wunderlist = Wunderlist()
        cls.wunderlist.login(EMAIL, PASSWORD)


class TestAPIRequests(TestAPI):
    def test_login(self):
        try:
            self.wunderlist.login(EMAIL, PASSWORD)
        except:
            self.fail("Login failure")

    def test_batch(self):
        '''Test a simple request using /batch'''
        me = api.calls.me()

        try:
            batch_results = self.wunderlist.send_requests([me])
        except:
            self.fail("Batch request failure")
        me_result = next(batch_results)

        # if we get a correct id value, everything probably worked on our end
        self.assertEqual(self.wunderlist.id, me_result["id"])

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
            results = self.wunderlist.send_requests([me, shares, services, events,
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
        self.assertEqual(self.wunderlist.id, me_result["id"])
        self.assertIn("background", settings_result)
        # not sure what's going on with services and events, so i won't check
        self.assertIn("background", settings_result)
        self.assertEqual(type(friends_result), list)  # can't do much more

    def test_tasks(self):
        '''Test all task related functionality'''
        import datetime

        due = datetime.date(2012, 12, 21).isoformat()
        add_task = api.calls.add_task("test", "inbox", due_date=due,
                                    starred=True)

        # sending a request now, because we need the list's id
        try:
            result = self.wunderlist.send_request(add_task)
        except:
            self.fail()
        new_task_id = result["id"]

        self.assertEqual(result["due_date"], due)
        self.assertEqual(result["title"], "test")
        self.assertEqual(result["starred"], True)

        # test adding a note and a reminder date
        add_note = api.calls.set_note_for_task("note", new_task_id)
        reminder = datetime.date(2012, 12, 22).isoformat()
        add_reminder = api.calls.set_reminder_for_task(new_task_id, reminder)
        complete_task = api.calls.complete_task(new_task_id)
        try:
            results = self.wunderlist.send_requests([add_note, add_reminder,
                                              complete_task])
        except:
            self.fail()

        note_result = next(results)
        reminder_result = next(results)
        complete_result = next(results)

        self.assertEqual(note_result["note"], "note")
        self.assertIsNotNone(complete_result["completed_at"])
        self.assertIsNotNone(complete_result["completed_by_id"])
        # test reminder date here

        # test getting tasks
        get_tasks = api.calls.get_all_tasks()
        try:
            result = self.wunderlist.send_request(get_tasks)
        except:
            self.fail()

        if len(result) < 1:
            self.fail("Received no tasks")
        if not any(t["title"] == "test" for t in result):
            self.fail("No test task found")

        # delete everything
        delete = api.calls.delete_task(new_task_id)
        try:
            self.wunderlist.send_request(delete)
        except:
            self.fail()

    def test_lists(self):
        '''Test list related stuff'''

        add_list = api.calls.add_list("test list")
        try:
            result = self.wunderlist.send_request(add_list)
        except:
            self.fail()

        list_id = result["id"]
        add_task = api.calls.add_task("test", list_id)
        try:
            result = self.wunderlist.send_request(add_task)
        except:
            self.fail()

        # check that the list exists and has a task in it
        get_lists = api.calls.get_lists()
        get_tasks = api.calls.get_all_tasks()
        try:
            results = self.wunderlist.send_requests([get_lists, get_tasks])
        except:
            self.fail()

        lists = next(results)
        tasks = next(results)

        if not any(l["title"] == "test list" for l in lists):
            self.fail()

        if not any(t["list_id"] == list_id for t in tasks):
            self.fail()

        task_id = result["id"]
        delete_task = api.calls.delete_task(task_id)
        delete_list = api.calls.delete_list(list_id)
        try:
            results = self.wunderlist.send_requests([delete_task, delete_list])
            next(results)
            next(results)
        except:
            self.fail()

    def test_comments(self):
        # add a task
        add_task = api.calls.add_task("comment test", "inbox")
        task_result = self.wunderlist.send_request(add_task)
        task_id = task_result["id"]
        # add a comment to the task
        add_comment = api.calls.add_comment("test", task_id)
        comment_result = self.wunderlist.send_request(add_comment)
        task_comments = self.wunderlist.send_request(api.calls.get_comments(task_id))
        # see if there's a comment with the title we gave
        self.assertEqual("test", task_comments[0]["text"])
        # cleanup
        delete = self.wunderlist.send_request(api.calls.delete_task(task_id))
