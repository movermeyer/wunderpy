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

    def inbox_id(self):
        lists = self.wunderlist.send_request(api.calls.get_lists())
        for l in lists:
            if l["title"] == "inbox":
                return l["id"]


class TestAvatarRequests(TestAPI):
    def test_get_avatar(self):
        '''Test GET /avatar'''

        get = api.calls.get_avatar(str(self.wunderlist.id))
        result = self.wunderlist.send_request(get)
        self.assertIsNotNone(result)


class TestFileRequests(TestAPI):
    pass


class TestListRequests(TestAPI):
    def setUp(self):
        add_list = api.calls.add_list("test list")
        result = self.wunderlist.send_request(add_list)
        self.list_id = result["id"]
        self.list_rev = result["revision"] + 2

        add_task = api.calls.add_task("test1", self.list_id)
        result = self.wunderlist.send_request(add_task)
        self.task_id = result["id"]
        self.task_rev = result["revision"]

    def tearDown(self):
        delete = api.calls.delete_task(self.task_id, self.task_rev)
        self.wunderlist.send_request(delete)

        self.list_rev += 1
        delete = api.calls.delete_list(self.list_id,
                                       self.list_rev)
        self.wunderlist.send_request(delete)

    def test_get_lists(self):
        lists = self.wunderlist.send_request(api.calls.get_lists())
        self.assertFalse(len(lists) < 2)

    def test_get_list(self):
        get_list = api.calls.get_list(self.list_id)
        l = self.wunderlist.send_request(get_list)
        self.assertEqual(l["title"], "test list")

    def test_get_task_count(self):
        get = api.calls.get_number_of_tasks(self.list_id)
        r = self.wunderlist.send_request(get)
        self.assertTrue((r["completed_count"] + r["uncompleted_count"])
                        > 0)

    def test_set_list_title(self):
        #self.list_rev += 1
        set_title = api.calls.set_list_title(self.list_id, "new",
                                             self.list_rev)
        r = self.wunderlist.send_request(set_title)
        self.assertEqual(r["title"], "new")
        self.list_rev = r["revision"]

    def test_set_list_public(self):
        #self.list_rev += 1
        set_public = api.calls.set_list_public(self.list_id,
                                               self.list_rev)
        r = self.wunderlist.send_request(set_public)
        self.assertEqual(r["public"], True)
        self.list_rev = r["revision"]


class TestMembership(TestAPI):
    def test_get_memberships(self):
        r = self.wunderlist.send_request(api.calls.get_memberships())

    def test_add_membership(self):
        add_list = api.calls.add_list("test list")
        result = self.wunderlist.send_request(add_list)
        list_id = result["id"]
        rev = result["revision"] + 1

        add = api.calls.add_to_list(self.wunderlist.id, list_id)
        r = self.wunderlist.send_request(add)

        self.wunderlist.send_request(api.calls.delete_list(list_id,
                                                           rev))


class TestNote(TestAPI):
    def setUp(self):
        add_task = api.calls.add_task("test1", self.inbox_id())
        result = self.wunderlist.send_request(add_task)
        self.task_id = result["id"]
        self.task_rev = result["revision"]

        add_note = api.calls.set_note_for_task(self.task_id, "note")
        r = self.wunderlist.send_request(add_note)
        self.note_id = r["id"]
        self.note_rev = r["revision"]

    def tearDown(self):
        delete = api.calls.delete_note(self.note_id, self.note_rev)
        self.wunderlist.send_request(delete)

        r = self.wunderlist.send_request(api.calls.get_task(self.task_id))
        self.task_rev = r["revision"]
        delete = api.calls.delete_task(self.task_id, self.task_rev)
        self.wunderlist.send_request(delete)

    def test_get_notes(self):
        r = self.wunderlist.send_request(api.calls.get_notes(self.task_id))
        self.assertTrue(len(r) > 0)

    def test_get_note(self):
        r = self.wunderlist.send_request(api.calls.get_note(self.note_id))
        self.assertEqual(r["content"], "note")

    def test_update_note(self):
        r = self.wunderlist.send_request(api.calls.update_note(self.note_id,
                                                               "asdf",
                                                               self.note_rev))
        r = self.wunderlist.send_request(api.calls.get_note(self.note_id))
        self.assertEqual(r["content"], "asdf")
        self.note_rev = r["revision"]


class TestPositions(TestAPI):
    def test_get_positions(self):
        self.wunderlist.send_request(api.calls.get_list_positions())


class TestReminder(TestAPI):
    def setUp(self):
        add_task = api.calls.add_task("test", self.inbox_id())
        result = self.wunderlist.send_request(add_task)
        self.task_id = result["id"]
        self.task_rev = result["revision"]

        remind = datetime.date(2012, 12, 22).isoformat()
        add_reminder = api.calls.set_reminder_for_task(self.task_id,
                                                       remind)
        self.task_rev
        r = self.wunderlist.send_request(add_reminder)
        self.reminder_id = r["id"]
        self.reminder_rev = r["revision"]

    def tearDown(self):
        delete_remind = api.calls.delete_reminder(self.reminder_id,
                                                  self.reminder_rev)
        self.wunderlist.send_request(delete_remind)
        delete = api.calls.delete_task(self.task_id, self.task_rev)
        self.wunderlist.send_request(delete)

    def test_get_reminders(self):
        get = api.calls.get_reminders(self.task_id)
        r = self.wunderlist.send_request(get)
        self.assertTrue(len(r) == 1)

    def test_update_reminder(self):
        new = "2015-03-17T00:00:00.000Z"
        update = api.calls.update_reminder(self.reminder_id, new,
                                           self.reminder_rev)
        r = self.wunderlist.send_request(update)
        self.assertEqual(r["date"], new)
        self.reminder_rev += 1


class TestSubtasks(TestAPI):
    def setUp(self):
        add_task = api.calls.add_task("test", self.inbox_id())
        result = self.wunderlist.send_request(add_task)
        self.task_id = result["id"]
        self.task_rev = result["revision"]

        add_sub = api.calls.add_subtask(self.task_id, "subtask")
        r = self.wunderlist.send_request(add_sub)
        self.sub_id = r["id"]
        self.sub_rev = r["revision"]

    def tearDown(self):
        delete = api.calls.delete_subtask(self.sub_id, self.sub_rev)
        self.wunderlist.send_request(delete)
        r = self.wunderlist.send_request(api.calls.get_task(self.task_id))
        self.task_rev = r["revision"]
        self.wunderlist.send_request(api.calls.delete_task(self.task_id,
                                                           self.task_rev))

    def test_get_subtasks(self):
        r = self.wunderlist.send_request(api.calls.get_subtasks(self.task_id))
        self.assertTrue(len(r) == 1)

    def test_get_subtask(self):
        call = api.calls.get_subtask(self.sub_id)
        r = self.wunderlist.send_request(call)
        self.assertEqual(r["title"], "subtask")

    def test_update_subtask_title(self):
        call = api.calls.update_subtask_title(self.sub_id,
                                              "asdf",
                                              self.sub_rev)
        r = self.wunderlist.send_request(call)
        self.assertEqual(r["title"], "asdf")
        self.sub_rev = r["revision"]

    def test_complete_subtask(self):
        call = api.calls.complete_subtask(self.sub_id, self.sub_rev)
        r = self.wunderlist.send_request(call)
        self.assertEqual(r["completed"], True)
        self.sub_rev = r["revision"]


class TestTasks(TestAPI):
    def setUp(self):
        add_task = api.calls.add_task("test", self.inbox_id())
        result = self.wunderlist.send_request(add_task)
        self.task_id = result["id"]
        self.task_rev = result["revision"]

    def tearDown(self):
        self.wunderlist.send_request(api.calls.delete_task(self.task_id,
                                                           self.task_rev))

    def test_get_tasks(self):
        get_tasks = api.calls.get_tasks(self.inbox_id())
        tasks = self.wunderlist.send_request(get_tasks)
        self.assertFalse(len(tasks) < 1)  # make sure we have one task

    def test_get_task(self):
        get_task = api.calls.get_task(self.task_id)
        r = self.wunderlist.send_request(get_task)
        self.assertEqual(r["title"], "test")

    def test_complete_task(self):
        complete_task = api.calls.complete_task(self.task_id, self.task_rev)
        complete = self.wunderlist.send_request(complete_task)
        self.assertTrue(complete["completed"])
        self.task_rev += 1

    def test_set_due_date(self):
        new = "2015-03-17"
        set_due = api.calls.set_task_due_date(self.task_id,
                                              new,
                                              self.task_rev)
        r = self.wunderlist.send_request(set_due)
        self.assertEqual(r["due_date"], new)
        self.task_rev += 1

    def test_set_recurring(self):
        call = api.calls.set_task_recurring(self.task_id, "day", 2,
                                            self.task_rev)
        r = self.wunderlist.send_request(call)
        self.assertEqual(r["recurrence_type"], "day")
        self.assertEqual(r["recurrence_count"], 2)
        self.task_rev += 1

    def test_set_title(self):
        call = api.calls.set_task_title(self.task_id, "asdf",
                                        self.task_rev)
        r = self.wunderlist.send_request(call)
        self.assertEqual(r["title"], "asdf")
        self.task_rev = r["revision"]


class TestTaskComments(TestAPI):
    def setUp(self):
        add_task = api.calls.add_task("comment test", self.inbox_id())
        task_result = self.wunderlist.send_request(add_task)
        self.task_id = task_result["id"]
        self.task_rev = task_result["revision"]

        add_comment = api.calls.add_comment("test", self.task_id)
        comment_result = self.wunderlist.send_request(add_comment)
        self.comment_id = comment_result["id"]
        self.task_rev += 1

    def tearDown(self):
        delete = api.calls.delete_task(self.task_id, self.task_rev)
        self.wunderlist.send_request(delete)

    def test_get_comments(self):
        task_comments = self.wunderlist.send_request(
            api.calls.get_comments(self.task_id))
        self.assertEqual("test", task_comments[0]["text"])

    def test_get_comment(self):
        send = api.calls.get_comment(self.comment_id)
        r = self.wunderlist.send_request(send)
        self.assertEqual(r["text"], "test")


class TestUpload(TestAPI):
    pass


class TestUser(TestAPI):
    def test_get_user(self):
        call = api.calls.get_user()
        self.wunderlist.send_request(call)
