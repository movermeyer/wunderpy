'''
.. module:: wunderlist
'''

from ._api import API, Request


class Wunderlist(object):
    '''A basic Wunderlist client.'''

    def __init__(self, email, password):
        '''
        :param email: The account's email address.
        :type email: str
        :param password: The account's password.
        :type password: str
        '''

        self._api = API()
        self._email = email
        self._password = password
        self._token = None
        self._id = None

        self.logged_in = False

        self.lists = []

    def login(self):
        '''Login to Wunderlist.'''

        user_data = self._api.login(self._email, self._password)
        self.logged_in = True
        self._token = user_data["token"]
        self._id = user_data["id"]

    def get_task_lists(self):
        '''Populate the lists with all tasks.'''

        # get tasks so we can add them to their appropriate list later
        tasks = self._api.send_request(Request.get_all_tasks())

        # get_lists() doesn't give us the inbox list, so we have to make it
        inbox = {}
        inbox["title"] = "inbox"
        inbox["id"] = "inbox"
        inbox["created_on"] = ""
        inbox["updated_on"] = ""
        inbox["tasks"] = [t for t in tasks if t["list_id"] == "inbox"]
        self.lists.append(inbox)
        
        # get the remaining lists and put the tasks into their list
        for list in self._api.send_request(Request.get_lists()):
            list["tasks"] = [t for t in tasks if t["list_id"] == list["id"]]
            self.lists.append(list)

    def add_task(self, title, list_title="inbox", note=None,
                 due_date=None, starred=False):
        '''Create a new task.
        
        :param title: The task's name.
        :type title: str
        :param list_title: The title of the list that the task will go in.
        :type list_title: str
        :param note: An additional note in the task.
        :type note: str or None
        :param due_date: The due date/time for the task in ISO format.
        :type due_date: str or None
        :param starred: If the task should be starred.
        :type starred: bool
        '''

        list_id = [l["id"] for l in self.lists if l["title"] == list_title][0]
        task = self._api.add_task(title, list_id, due_date=due_date,
                                  starred=starred)

        if note:
            self._api.set_note_for_task(task)
