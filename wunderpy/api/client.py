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
            return r.json()
        elif r.status_code == 404:  # dirty hack around this timing bullshit
            time.sleep(1)
            r2 = self.session.send(request.prepare(), timeout=timeout)
            if r2.status_code == 404:  # still doesn't work
                raise Exception(r2.status_code, r2)
            else:
                return r2.json()
        else:
            raise Exception(r.status_code, r)
