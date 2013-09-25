'''
.. module:: api
'''

from .request import Request
import requests


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
    '''

    def __init__(self, request_timeout=30):
        '''
        :param request_timeout: Timeout value (seconds) for all requests.
        :type request_timeout: int
        '''

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

        user_info = self.send_request(Request.login(email, password))
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

        request_url = "{}{}".format(request.api_server, request.path)
        __send_request = function_for_request_method(request.method)
        r = __send_request(request_url, data=request.body_json,
                           headers=self.header, timeout=self.timeout)
        if r.status_code < 300:
            return r.json()
        else:
            raise Exception(r.status_code)

    def send_requests(self, api_requests):
        '''Sends requests as a batch.

        Returns a generator which will yield the server response for each
        request in the order they were supplied.

        :param api_requests: a list of Valid Request objects.
        :type api_requests: list
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
