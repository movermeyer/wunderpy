'''
.. module:: request
'''


import json
import datetime


class Request(object):
    '''Object representing a single request.'''
    def __init__(self, method, path, body,
                 api_server="https://api.wunderlist.com"):
        '''
        :param method: HTTP method to use.
        :type method: str
        :param path: URL path for the API call. Must have prefix /.
        :type path: str
        :param body: The HTTP request's data/body.
        :type body: dict
        :param api_server: The server the request will be sent to.
        "type api_server: str
        '''

        self.api_server = api_server
        self.method = method
        self.path = path
        if not body:
            self.body = {}
        else:
            self.body = body
        self.body_json = json.dumps(body)

    def __repr__(self):
        return "<wunderpy Request: {} {}>".format(self.method, self.path)

    def batch_format(self):
        op = {"method": self.method, "url": self.path,
              "params": self.body}
        return op

    @classmethod
    def login(self, email, password):
        '''Login request, so we can get a token.

        :returns: Request
        '''

        return Request("POST", "/login",
                       body={"email": email, "password": password})

    @classmethod
    def me(self):
        '''Request for /me, which returns user information.

        :returns: Request
        '''

        return Request("GET", "/me", body=None)

    @classmethod
    def get_all_tasks(self):
        '''Get every task associated with the account.

        :returns: Request
        '''

        return Request("GET", "/me/tasks", body=None)

    @classmethod
    def add_task(self, title, list_id, due_date=None, starred=False):
        '''Add a task to a list.

        :param title: The task name/title.
        :type title: str
        :param list_id: id of the list to put the task in.
        :type list_id: str
        :param due_date: Date the task will be due in ISO format
        :type due_date: str
        :param starred: Whether the task should be starred.
        :type starred: bool
        :returns: Request
        '''

        if starred is False:
            starred = 0
        elif starred is True:
            starred = 1

        body = {"list_id": list_id, "title": title, "starred": starred}
        if due_date:
            body["due_date"] = due_date  # should be in ISO format

        return Request("POST", "/me/tasks", body)

    @classmethod
    def complete_task(self, task_id, completed_at=None):
        '''Mark a task as completed.
            
        :param task_id: The ID of the task you are completing.
        :type task_id: str
        :param completed_at: The datetime it was completed at, in ISO format.
        :type completed_at: str
        '''

        if not completed_at:
            completed_at = datetime.datetime.now().isoformat()

        path = "/{}".format(task_id)
        body = {"completed_at": completed_at, "position": 0}
        return Request("PUT", path, body=body)

    @classmethod
    def set_note_for_task(self, note, task_id):
        '''Set a task's note field.

        :param note: The note's contents.
        :type note: str
        :param task_id: The id of the task.
        :type task_id: str
        :returns: Request
        '''

        path = "/{}".format(task_id)
        body = {"note": note}
        return Request("PUT", path, body)

    @classmethod
    def set_task_due_date(self, task_id, due_date, recurrence_count=1):
        '''Set a task's due date.

        :param task_id: The id of the task.
        :type task_id: str
        :param due_date: The new due date in ISO format.
        :type due_date: str
        :param recurrence_count: Not completely sure yet.
        :type recurrence_count: int
        :returns: Request
        '''

        path = "/{}".format(task_id)
        body = {"due_date": due_date, "recurrence_count": recurrence_count}
        return Request("PUT", path, body)

    @classmethod
    def delete_task(self, task_id):
        '''Delete a task.

        :param task_id: The task's id.
        :type task_id: str
        :returns: Request
        '''

        path = "/{}".format(task_id)
        return Request("DELETE", path, body=None)

    @classmethod
    def get_lists(self):
        '''Get all of the task lists

        :returns: Request
        '''

        return Request("GET", "/me/lists", body=None)

    @classmethod
    def add_list(self, list_name):
        '''Create a new task list.

        :param list_name: The name of the new list.
        :type list_name: str
        :returns: Request
        '''

        body = {"title": list_name}
        return Request("POST", "/me/lists", body)

    @classmethod
    def delete_list(self, list_id):
        '''Delete a list and all of its contents.

        :param list_id: The id of the list to delete.
        :type list_id: str
        :returns: Request
        '''

        list_path = "/{}".format(list_id)
        return Request("DELETE", list_path, body=None)

    @classmethod
    def get_comments(self, task_id):
        '''Get all comments from the specified task.
        
        :param task_id: The ID of the task.
        :type task_id: str
        '''

        url = "https://comments.wunderlist.com"
        path = "/tasks/{}/messages".format(task_id)
        return Request("GET", path, body=None, api_server=url)

    @classmethod
    def add_comment(self, title, task_id):
        '''Add a comment to a task. I'm not sure if this works with batch
        
        :param title: The comment name/title.
        :param task_id: The ID of the task you're commenting on.
        :type title: str
        :type task_id: str
        :returns: Request
        '''

        url = "https://comments.wunderlist.com"
        body = {"channel_id": task_id, "channel_type": "tasks",
                "text": title}
        path = "/tasks/{}/messages".format(task_id)
        return Request("POST", path, body=body, api_server=url)

    @classmethod
    def get_reminders(self):
        '''Get a list of all reminders.

        :returns: Request
        '''

        return Request("GET", "/me/reminders", body=None)

    @classmethod
    def set_reminder_for_task(self, task_id, date):
        '''Add a reminder for a task.

        :param task_id: The id of the task.
        :type task_id: str
        :param date: The reminder date/time in ISO format.
        :type date: str
        :returns: Request
        '''

        body = {"task_id": task_id, "date": date}  # date is in ISO date format
        return Request("POST", "/me/reminders", body)

    @classmethod
    def get_shares(self):
        '''Get a list of all things shared with you, I think...

        :returns: Request
        '''

        return Request("GET", "/me/shares", body=None)

    @classmethod
    def get_services(self):
        '''Not sure.

        :returns: Request
        '''

        return Request("GET", "/me/services", body=None)

    @classmethod
    def get_events(self):
        '''Not sure.

        :returns: Request
        '''

        return Request("GET", "/me/events", body=None)

    @classmethod
    def get_settings(self):
        '''Get account settings.

        :returns: Request
        '''

        return Request("GET", "/me/settings", body=None)

    @classmethod
    def get_friends(self):
        '''Get friends list.

        :returns: Request
        '''

        return Request("GET", "/me/friends", body=None)
