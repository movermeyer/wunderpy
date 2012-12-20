from ._wunderlist_api import API


class Wunderlist(object):
    def __init__(self, email, password):
        self.api = API()
        self.email = email
        self.password = password
        self.logged_in = False
        self.user_data = None

    def login(self):
        self.user_data = self.api.login(self.email, self.password)
        return True  # an exception will be raised if logging in didn't work
