'''
.. module:: wunderlist
'''

from wunderpy import api
from requests import Session


class Wunderlist(api.APIClient):
    '''A basic Wunderlist client.'''

    def __init__(self):
        api.APIClient.__init__(self)
        self.lists = {}

    def init_lists(self):
        '''Populate the lists with all tasks.'''

        request = self.send_requests([api.calls.get_all_tasks(),
                                          api.calls.get_lists()])
        tasks = next(request)
        lists = next(request)

        inbox = {"title": "inbox", "id": "inbox", "created_on": None,
                 "updated_on": None}
        inbox["tasks"] = [t for t in tasks if t["list_id"] == "inbox"]
        self.lists["inbox"] = inbox

        for list in lists:
            list["tasks"] = [t for t in tasks if t["list_id"] == list["id"]]
            self.lists[list["title"]] = list

    def tasks_for_list(self, list_title):
        '''Get all tasks belonging to a list.'''

        return self.lists[list_title].get("tasks")

    def add_task(self, title, list="inbox", note=None, due_date=None,
                 starred=False):
        '''Create a new task.

        :param title: The task's name.
        :type title: str
        :param list: The title of the list that the task will go in.
        :type list: str
        :param note: An additional note in the task.
        :type note: str or None
        :param due_date: The due date/time for the task in ISO format.
        :type due_date: str or None
        :param starred: If the task should be starred.
        :type starred: bool
        '''

        list_id = self.lists[list]["id"]
        add_task = api.calls.add_task(title, list_id, due_date=due_date,
                                      starred=starred)
        result = self.send_request(add_task)

        if note:
            self.send_request(api.calls.set_note_for_task(note, result["id"]))

    def complete_task(self, task_title, list):
        '''Complete a task with the given title in the given list.'''


        self.send_request(api.calls.complete_task())
