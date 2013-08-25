'''
.. module:: _api
'''

import requests
import json


class API(object):
    '''Ultimately handles all calls to Wunderlist.
        
    This class simply provides facilities for sending requests using the batch
    api or regular "real-time" requests. See the Request class and its
    class methods for objects encapsulating certain API calls, those objects
    can then be passed to send_request or send_requests.
    
    .. note::
        All requests (except for login) require an authentication header
        using a token received from the login request.
        The values to go into the header are
        {"Authorization": "Bearer " + token}.

    .. |url| replace:: API_URL
    '''

    def __init__(self, url="https://api.wunderlist.com", 
                 request_timeout=30):
        '''
        :param url: URL of the API that will be used.
        :type url: str
        :param request_timeout: Timeout value (seconds) for all requests.
        :type request_timeout: int
        '''

        self.api_url = url
        self.timeout = request_timeout
        self.header = {"Content-Type": "application/json"}

    def login(self, email, password):
        '''Login to Wunderlist.
    
        :param email: The account's email address.
        :type email: str
        :param password: The account's password.
        :type password: str
        :returns: dict -- Containing user information.
        '''
    
        request_body = {"email": email, "password": password}
        user_info = self.send_request(Request("POST", "/login", request_body))
        self.header["Authorization"] = "Bearer " + user_info["token"]
        return user_info
        
    def send_request(self, request):
        '''Send a single request to Wunderlist in real time.
        
        :param request: A valid Request object for the request.
        :type request_method: Request
        :returns: dict:
        '''
    
        def function_for_request_method(method):
            if method == "GET":
                return requests.get
            elif method == "POST":
                return requests.post
            elif method == "PUT":
                return requests.put
            elif method == "DELETE":
                return requests.delete
        
        request_url = "{}{}".format(self.api_url, request.path)
        __send_request = function_for_request_method(request.method)
        r = __send_request(request_url, data=request.body_json,
                           headers=self.header, timeout=self.timeout)
        if r.status_code < 300:
            return r.json()
        else:
            raise Exception(r.status_code)


    def send_requests(self, *api_requests):
        '''Sends requests as a batch.        
    
        Returns a generator which will yield the server response for each
        request in the order they were supplied.
        
        :param api_requests: Valid Request objects.
        :type requests: Request
        :yields: dict
        '''
    
        ops = [req.batch_format() for req in api_requests]
    
        request_body = {"ops": ops, "sequential": True}
        batch_request = Request("POST", "/batch", request_body)
        responses = self.send_request(batch_request)
        for response in responses["results"]:
            if response["status"] < 300:  # /batch is always 200
                yield response["body"]
            else:
                raise Exception(response["status"]) 

class Request(object):
    '''Object representing a single request.'''
    def __init__(self, method, path, body):
        '''
        :param method: HTTP method to use.
        :type method: str
        :param path: URL path for the API call. Must have prefix /.
        :type path: str
        :param body: The HTTP request's data/body.
        :type body: dict
        '''
        self.method = method
        self.path = path
        if not body:
            self.body = {}
        else:
            self.body = body
        self.body_json = json.dumps(body)

    def batch_format(self):
        op = {"method": self.method, "url": self.path, \
              "params": self.body}
        return op

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
        :returns: dict
        '''
    
        list_path = "/{}".format(list_id)
        return Request("DELETE", list_path, body=None)
    
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
