import requests


class API(object):
    def __init__(self, url="https://api.wunderlist.com", request_timeout=30):
        self.api_url = url
        self.timeout = request_timeout
        self.token = None  # needed for just about everything, so we'll save it
        self.header = None  # needed for almost every request

    def login(self, email, password):
        login_url = self.api_url + "/login"
        request_body = {"email": email, "password": password}

        login_request = requests.post(login_url, data=request_body,
                                      timeout=self.timeout)
        if login_request.status_code == 200:  # All good
            user_info = login_request.json()
            self.token = user_info["token"]

            # reporting as the mac app here because there isn't a public API
            self.header = {"Authorization": "Bearer " + self.token,
                           "Content-Type": "application/json; charset=utf-8",
                           "Accept-Encoding": "gzip",
                           "X-6W-Product": "Wunderlist",
                           "X-6W-Product-Version": "2.0",
                           "X-6W-Platform": "Mac",
                           "X-6W-System": "x86_64",
                           "X-6W-System-Version": "12C54"}

            return user_info
        else:
            raise Exception("Login error", login_request.status_code)

    def me(self):
        me_url = self.api_url + "/me"
        me_request = requests.get(me_url, headers=self.header)

        if me_request.status_code == 200:
            return me_request.json()
        else:
            raise Exception("Get me error", me_request.status_code)

    def get_all_tasks(self):
        tasks_url = self.api_url + "/me/tasks"
        tasks_request = requests.get(tasks_url, headers=self.header)

        if tasks_request.status_code == 200:
            return tasks_request.json()
        else:
            raise Exception("Get tasks error", tasks_request.status_code)

    def add_task(self, title, list_id, due_date=None, starred=False):
        if starred is False:
            starred = 0
        elif starred is True:
            starred = 1

        tasks_url = self.api_url + "/me/tasks"
        body = {"list_id": list_id, "title": title, "starred": starred}
        if due_date:
            body["due_date"] = due_date  # should be in ISO format
        tasks_request = requests.post(tasks_url, data=body,
                                      headers=self.header)

        if tasks_request.status_code == 201:  # Created
            return tasks_request.json()
        else:
            raise Exception("Add task error", tasks_request.status_code)

    def set_note_for_task(self, note, task_id):
        task_url = self.api_url + "/" + task_id
        body = {"note": note}
        task_request = requests.put(task_url, data=body,
                                    headers=self.header)

        if task_request.status_code == 200:
            return task_request.json()  # new task info
        else:
            raise Exception("Set task note error", task_request.status_code)

    def delete_task(self, task_id):
        task_url = self.api_url + "/" + task_id
        task_request = requests.delete(task_url, headers=self.header)

        if task_request.status_code == 200:
            return True  # server doesn't respond with anything
        else:
            raise Exception("Delete task error", task_request.status_code)

    def get_lists(self):
        lists_url = self.api_url + "/me/lists"
        lists_request = requests.get(lists_url, headers=self.header)

        if lists_request.status_code == 200:
            return lists_request.json()
        else:
            raise Exception("Get lists error", lists_request.status_code)

    def add_list(self, list_name):
        lists_url = self.api_url + "/me/lists"
        body = {"title": list_name}
        list_request = requests.post(lists_url, data=body,
                                     headers=self.header)

        if list_request.status_code == 201:
            return list_request.json()
        else:
            raise Exception("Add list error", list_request.status_code)

    def delete_list(self, list_id):
        list_url = self.api_url + "/" + list_id
        list_request = requests.delete(list_url, headers=self.header)

        if list_request.status_code == 200:
            return True
        else:
            raise Exception("Delete list error", list_request.status_code)

    def get_reminders(self):
        reminders_url = self.api_url + "/me/reminders"
        reminders_request = requests.get(reminders_url, headers=self.header)

        if reminders_request.status_code == 200:
            return reminders_request.json()
        else:
            raise Exception("Get reminders error",
                            reminders_request.status_code)

    def get_shares(self):
        shares_url = self.api_url + "/me/shares"
        shares_request = requests.get(shares_url, headers=self.header)

        if shares_request.status_code == 200:
            return shares_request.json()
        else:
            raise Exception("Get shares error", shares_request.status_code)

    def get_services(self):
        services_url = self.api_url + "/me/services"
        services_request = requests.get(services_url, headers=self.header)

        if services_request.status_code == 200:
            return services_request.json()
        else:
            raise Exception("Get services error", services_request.status_code)

    def get_events(self):
        events_url = self.api_url + "/me/events"
        events_request = requests.get(events_url, headers=self.header)

        if events_request.status_code == 200:
            return events_request.json()
        else:
            raise Exception("Get events error", events_request.status_code)

    def get_settings(self):
        settings_url = self.api_url + "/me/settings"
        settings_request = requests.get(settings_url, headers=self.header)

        if settings_request.status_code == 200:
            return settings_request.json()
        else:
            raise Exception("Get settings error", settings_request.status_code)

    def get_friends(self):
        friends_url = self.api_url + "/me/friends"
        friends_request = requests.get(friends_url, headers=self.header)

        if friends_request.status_code == 200:
            return friends_request.json()
        else:
            raise Exception("Get friends error", friends_request.status_code)
