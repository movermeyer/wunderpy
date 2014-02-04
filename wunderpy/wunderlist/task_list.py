class TaskList(dict):
    '''Object representing a single task list in Wunderlist.'''

    def __init__(self, info, tasks=[], *args):
        '''
        :param tasks: A list of Task objects this list contains.
        :type tasks: list
        :param info: Information dict about the list returned by the API.
        :type info: dict
        '''

        self.tasks = tasks
        self.info = info
        dict.__init__(self, args)

    def __getitem__(self, key):
        return dict.__getitem__(self.info, key)

    def __setitem__(self, key, value):
        dict.__setitem__(self.info, key, value)

    def __repr__(self):
        return "<wunderpy.wunderlist.TaskList: {} {}>".format(self.title,
                                                              self.id)

    @property
    def title(self):
        return self.info.get("title")

    @property
    def id(self):
        return self.info.get("id")

    def add_task(self, task):
        '''Add a Task to the list.'''
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def task_with_title(self, title):
        tasks = self.tasks_with_title(title)
        if len(tasks) >= 1:
            #return most recent task
            tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
            return tasks[0]
        else:
            return None

    def tasks_with_title(self, title):
        '''Find all Tasks with the given title.
        :param title: Title to match Tasks with.
        :type title: str
        '''

        return filter(lambda task: task.title == title, self.tasks)

    def tasks_due_before(self, date):
        '''Find all Tasks that are due before date.'''

        return filter(lambda task: task.due_date and task.due_date < date,
                      self.tasks)

    def tasks_due_on(self, date):
        '''Find all Tasks that are due on date.'''

        return filter(lambda task: task.due_date and task.due_date == date,
                      self.tasks)

    def incomplete_tasks(self):
        return filter(lambda task: task.completed is not True, self.tasks)
