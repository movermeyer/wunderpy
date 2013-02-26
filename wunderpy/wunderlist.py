'''
.. module:: wunderlist
'''

from ._api import API


class Wunderlist(object):
    '''A basic Wunderlist client.
    
    This wraps the calls from :class:`API`.
    '''

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
        '''Login to Wunderlist.
        
        :returns: bool -- If the login was successful.
        '''

        user_data = self._api.login(self._email, self._password)
        self.logged_in = True
        self._token = user_data["token"]
        self._id = user_data["id"]

        return True  # an exception will be raised if logging in didn't work

    def get_task_lists(self):
        '''Populate the lists with all tasks.
        
        :returns: bool -- If it was able to acquire the tasks.
        '''

        # get tasks so we can add them to their appropriate list later
        tasks = []
        for i in self._api.get_all_tasks():
            filtered_task = {}
            filtered_task["title"] = i["title"]
            filtered_task["owner"] = i["owner_id"]
            filtered_task["list"] = i["list_id"]
            filtered_task["starred"] = i["starred"]
            filtered_task["due_date"] = i["due_date"]
            filtered_task["id"] = i["id"]
            filtered_task["note"] = i["note"]
            filtered_task["completed"] = i["completed_at"]
            filtered_task["last_updated"] = i["updated_at"]
            filtered_task["recurrence_count"] = i["recurrence_count"]
            filtered_task["recurrence_type"] = i["recurrence_type"]
        
            tasks.append(filtered_task)

        # get_lists() doesn't give us the inbox list, so we have to make it
        inbox = {}
        inbox["title"] = "inbox"
        inbox["id"] = "inbox"
        inbox["created_on"] = ""
        inbox["updated_on"] = ""
        inbox["tasks"] = [t for t in tasks if t["list"] == "inbox"]
        self.lists.append(inbox)
        
        # get the remaining lists and put the tasks into their list
        for i in self._api.get_lists():
            filtered_list = {}
            filtered_list["title"] = i["title"]
            filtered_list["created_on"] = i["created_at"]
            filtered_list["updated_on"] = i["updated_at"]
            filtered_list["id"] = i["id"]
            filtered_list["tasks"] = \
                [t for t in tasks if t["list"] == i["id"]]
        
            self.lists.append(filtered_list)

        return True

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
        :returns: bool -- If it was able to add the task.
        '''

        list_id = [l["id"] for l in self.lists if l["title"] == list_title][0]
        task = self._api.add_task(title, list_id, due_date=due_date,
                                  starred=starred)

        if note:
            task
            self._api.set_note_for_task()

        return True

