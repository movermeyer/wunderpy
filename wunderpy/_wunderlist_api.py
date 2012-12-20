import requests


class API(object):
    def __init__(self, url="https://api.wunderlist.com", request_timeout=30):
        self.api_url = url
        self.timeout = request_timeout

    def login(self, email, password):
        login_url = self.api_url + "/login"
        request_body = {"email": email, "password": password}

        login_request = requests.post(login_url, data=request_body,
                                      timeout=self.timeout)
        if login_request.status_code == 200:  # All good
            return login_request.json()
        else:
            raise Exception("Login error", login_request.status_code)

    def get_tasks(self, token):
        if not token:
            raise Exception("Auth token needed")

        tasks_url = self.api_url + "/inbox/tasks"
        auth_header = {"Authorization": "Bearer " + token}

        tasks_request = requests.get(tasks_url, headers=auth_header)

        if tasks_request.status_code == 200:
            return tasks_request.json()
        else:
            raise Exception("Get tasks error", tasks_request.status_code)
