'''Facilities for a client that only sends requests to the Wunderlist API'''

import json
import time

from requests import Session

from wunderpy.api.calls import API_URL
from wunderpy.api.calls import login as login_call


class APIClient(object):
    '''A class implementing all of the features needed to talk to Wunderlist'''

    def __init__(self, client_id):
        self.session = Session()
        self.token = None
        self.client_id = client_id
        self.id = None
        self.headers = {"Content-Type": "application/json",
                        "X-Client-ID": client_id}

    def login(self, email, password):
        '''Login to wunderlist'''

        r = self.send_request(login_call(email, password, self.client_id))
        self.set_token(r["access_token"])
        self.id = r["id"]

    def set_token(self, token):
        '''Set token manually to avoid having to login repeatedly'''
        self.token = token
        self.headers["X-Access-Token"] = token

    def send_request(self, request, timeout=30):
        '''Send a single request to Wunderlist in real time.

        :param request: A prepared Request object for the request.
        :type request_method: Request
        :param timeout: Timeout duration in seconds.
        :type timeout: int
        :returns: dict:
        '''

        request.headers = self.headers
        # Include the session headers in the request
        request.headers.update(self.session.headers)
        if request.data == []:
            request.data = json.dumps({})
        else:
            request.data = json.dumps(request.data)

        r = self.session.send(request.prepare(), timeout=timeout)

        if r.status_code < 300:
            try:
                return r.json()
            except UnicodeDecodeError:
                return r.text
            except ValueError:
                return r.text
        else:
            raise Exception(r.status_code, r, r.text)

    def send_requests(self, requests, timeout=30):
        for r in requests:
            yield self.send_request(r, timeout=timeout)
