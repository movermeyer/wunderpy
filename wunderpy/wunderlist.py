from ._wunderlist_api import API


class Wunderlist(object):
    def __init__(self, email, password):
        self.api = API()
        self.email = email
        self.password = password
        self.logged_in = False
        self.token = None
        self.id = None

        self.current_tasks = None

    def login(self):
        user_data = self.api.login(self.email, self.password)
        self.logged_in = True
        self.token = user_data["token"]
        self.id = user_data["id"]

        self.current_tasks = self.api.get_tasks()

        return True  # an exception will be raised if logging in didn't work
