import unittest
from datetime import date, datetime, timedelta

from wunderpy import Wunderlist
from wunderpy.wunderlist.task_list import TaskList
from wunderpy.wunderlist.task import Task


class TestClient(unittest.TestCase):
    def setUp(self):
        self.wl = Wunderlist()

        # not calling update_lists, because it sends requests
        inbox_info = {"title": "inbox", "id": "inbox", "created_on": None,
                      "updated_on": None}
        self.inbox = TaskList(info=inbox_info)
        self.wl.lists.append(self.inbox)

    def test_list_filter(self):
        list_one = TaskList(info={"title": "one", "id": "one"})
        self.wl.lists.append(list_one)

        list_two = TaskList(info={"title": "one", "id": "two"})
        self.wl.lists.append(list_two)

        self.assertEqual(self.wl.list_with_title("inbox"), self.inbox)
        self.assertEqual(self.wl.lists_with_title("one"),
                         [list_one, list_two])

        self.wl.lists.remove(list_one)
        self.wl.lists.remove(list_two)

    def test_get_tasks(self):
        task = Task({"title": "title", "id": "id"})
        self.inbox.add_task(task)
        self.assertEqual(self.wl.tasks_for_list("inbox"), [task])
        self.assertEqual(self.wl.get_task("title", "inbox"), task)
        self.assertEqual(self.wl.id_for_task("title", "inbox"), "id")

    def test_lists(self):
        one = TaskList({"title": "one", "id": "one"})
        self.wl.lists.append(one)
        two = TaskList({"title": "one", "id": "two"})
        self.wl.lists.append(two)

        self.assertEqual(self.wl.list_with_title("inbox"), self.inbox)
        self.assertEqual(self.wl.lists_with_title("one"), [one, two])
        self.assertEqual(self.wl.id_for_list("inbox"), "inbox")

    def test_due_before(self):
        one = TaskList({"title": "one", "id": "one"})
        task_one = Task({"title": "task1", "id": "one",
                        "due_date": (date.today() -
                                     timedelta(days=1)).isoformat()})
        one.add_task(task_one)
        self.wl.lists.append(one)

        two = TaskList({"title": "two", "id": "two"})
        task_two = Task({"title": "two", "id": "two",
                        "due_date": (date.today() +
                                     timedelta(days=1)).isoformat()})
        two.add_task(task_two)
        self.wl.lists.append(two)

        task_three = Task({"title": "three", "id": "three",
                          "due_date": (date.today() +
                                       timedelta(days=1)).isoformat()})
        self.inbox.add_task(task_three)

        self.assertEqual(self.wl.tasks_due_before(date.today()), [task_one])
        self.assertEqual(self.wl.tasks_due_before(date.today() +
                                                  timedelta(days=2)),
                         [task_one, task_two, task_three])

    def test_due_on(self):
        one = TaskList({"title": "one", "id": "one"})
        task_one = Task({"title": "task1", "id": "one",
                        "due_date": (date.today() -
                                     timedelta(days=1)).isoformat()})
        one.add_task(task_one)
        self.wl.lists.append(one)

        two = TaskList({"title": "two", "id": "two"})
        task_two = Task({"title": "two", "id": "two",
                        "due_date": (date.today().isoformat())})
        two.add_task(task_two)
        self.wl.lists.append(two)

        task_three = Task({"title": "three", "id": "three",
                          "due_date": (date.today() +
                                       timedelta(days=1)).isoformat()})
        self.inbox.add_task(task_three)

        self.assertEqual(self.wl.tasks_due_on(date.today()), [task_two])
        self.assertEqual(self.wl.tasks_due_on(date.today() +
                                              timedelta(days=1)),
                         [task_three])


class TestTaskList(unittest.TestCase):
    def setUp(self):
        info = {"title": "inbox", "id": "inbox", "created_on": None,
                "updated_on": None}
        self.test_list = TaskList(info=info)

    def test_info(self):
        '''Ensure that the dict from Wunderlist is retained.'''

        info = {"title": "inbox", "id": "inbox", "created_on": None,
                "updated_on": None}
        self.assertEqual(self.test_list.info, info)

    def test_properties(self):
        '''Test that all TaskList properties work.'''

        self.assertEqual(self.test_list.title, self.test_list.info["title"])
        self.assertEqual(self.test_list.id, self.test_list.info["id"])

    def test_modifying(self):
        '''Test adding and removing tasks.'''

        # adding
        task = Task(parent_list=self.test_list, info={"title": "task"})
        self.test_list.add_task(task)
        self.assertEqual(self.test_list.tasks, [task])

        # removing
        self.test_list.remove_task(task)
        self.assertEqual(self.test_list.tasks, [])

        self.test_list["title"] = "new_title"
        self.assertEqual(self.test_list.title, "new_title")
        self.test_list["title"] = "title"

    def test_title_filtering(self):
        one = Task({"title": "one", "id": "one",
                    "created_at": datetime.now().isoformat()})
        two = Task({"title": "two", "id": "two"})
        three = Task({"title": "one", "id": "three",
                      "created_at": datetime.now().isoformat()})
        self.test_list.add_task(one)
        self.test_list.add_task(two)
        self.test_list.add_task(three)

        self.assertEqual(self.test_list.task_with_title("one"), three)
        self.assertEqual(self.test_list.task_with_title("two"), two)
        self.assertEqual(self.test_list.tasks_with_title("one"), [one, three])


    def test_date_filtering(self):
        now = date.today()
        yesterday = now - timedelta(days=1)
        before = Task(info={"title": "before",
                            "due_date": yesterday.isoformat()})
        today = Task(info={"title": "today",
                           "due_date": now.isoformat()})
        tomorrow = now + timedelta(days=1)
        after = Task(info={"title": "after",
                           "due_date": tomorrow.isoformat()})
        self.test_list.add_task(before)
        self.test_list.add_task(today)
        self.test_list.add_task(after)

        self.assertEqual(self.test_list.tasks_due_before(now),
                         [before])
        self.assertEqual(self.test_list.tasks_due_on(now),
                         [today])

    def test_incomplete_tasks(self):
        one = Task({"title": "one", "completed_at": "date"})
        two = Task({"title": "two", "id": "two"})  # not completed
        self.test_list.add_task(one)
        self.test_list.add_task(two)

        self.assertEqual(self.test_list.incomplete_tasks(), [one])


class TestTask(unittest.TestCase):
    def setUp(self):
        self.due = date.today()
        self.now = datetime.now()
        self.info = {"title": "task", "id": "task",
                     "due_date": self.due.isoformat(),
                     "completed_at": None,
                     "created_at": self.now.isoformat()}
        self.task = Task(info=self.info)

    def test_properties(self):
        self.assertEqual(self.task.title, self.info["title"])
        self.assertEqual(self.task.id, self.info["id"])
        self.assertEqual(self.task.due_date, self.due)
        self.assertEqual(self.task.completed, False)
        self.assertEqual(self.task.created_at, self.now)
