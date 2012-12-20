import requests


class API(object):
    def __init__(self, url='https://api.wunderlist.com', request_timeout=30):
        self.api_url = url
        self.timeout = request_timeout

    def login(self, email, password):
        login_url = self.api_url + '/login'
        request_body = {"email": email, "password": password}

        login_request = requests.post(login_url, data=request_body,
                                      timeout=self.timeout)
        if login_request.status_code == 200:  # All good
            return login_request.json()
        else:
            raise Exception("Login error", login_request.status_code)
