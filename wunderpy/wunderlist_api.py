import requests


class Wunderlist(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.api_url = "https://api.wunderlist.com"
        self.logged_in = False
        self.user_data = None

    def login(self):
        login_url = self.api_url + "/login"
        payload = {"email": self.email, "password": self.password}

        r = requests.post(login_url, data=payload)
        if r.status_code != 200:
            raise Exception
        else:
            self.logged_in = True
            self.user_data = r.json()

            return True
