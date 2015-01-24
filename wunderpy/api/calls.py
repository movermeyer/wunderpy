'''
.. module:: calls
'''

import datetime
from requests import Request


API_URL = "https://a.wunderlist.com/api/v1"


def login(email, password):
    '''Login request, so we can get a token.

    :returns: Request
    '''

    return Request("POST", "{}/login".format(API_URL),
                   data={"email": email, "password": password})


def get_user():
    '''Request for /user, which returns user information.

    :returns: Request
    '''

    return Request("GET", "{}/user".format(API_URL))


def get_tasks(list_id, completed=False):
    '''Get tasks in a list.

    :param list_id: The list'd ID.
    :param completed: Return only completed tasks.
    :returns: Request
    '''

    body = {"list_id": list_id, "completed": completed}
    return Request("GET", "{}/tasks".format(API_URL), data=body)


def get_task(task_id):
    '''Get all information for a given task.

    :param task_id: The tasks'd ID.
    :returns: Request
    '''

    return Request("GET", "{}/tasks/{}".format(API_URL, task_id))


def add_task(title, list_id, due_date=None, starred=False):
    '''Add a task to a list.

    :param title: The task name/title.
    :type title: str
    :param list_id: id of the list to put the task in.
    :type list_id: str
    :param due_date: Date the task will be due in ISO format
    :type due_date: str
    :param starred: Whether the task should be starred.
    :type starred: bool
    :returns: Request
    '''

    body = {"list_id": list_id, "title": title, "starred": int(starred)}
    if due_date:
        body["due_date"] = due_date  # should be in ISO format

    return Request("POST", "{}/tasks".format(API_URL), data=body)


def complete_task(task_id, revision):
    '''Mark a task as completed.

    :param task_id: The ID of the task you are completing.
    :type task_id: str
    :param revision: The task's revision number.
    :returns: Request
    '''

    url = "{}/tasks/{}".format(API_URL, task_id)
    body = {"revision": revision}
    return Request("PATCH", url, data=body)


def set_note_for_task(task_id, note):
    '''Set a task's note field.

    :param task_id: The id of the task.
    :type task_id: str
    :param note: The note's contents.
    :type note: str
    :returns: Request
    '''

    url = "{}/notes".format(API_URL)
    body = {"content": note, "task_id": task_id}
    return Request("POST", url, data=body)


def set_task_due_date(task_id, due_date, revision):
    '''Set a task's due date.

    :param task_id: The id of the task.
    :type task_id: str
    :param due_date: The new due date in ISO format.
    :type due_date: str
    :param revision: The tasks's revision number.
    :returns: Request
    '''

    url = "{}/tasks/{}".format(API_URL, task_id)
    body = {"due_date": due_date, "revision": revision}
    return Request("PATCH", url, data=body)


def delete_task(task_id, revision):
    '''Delete a task.

    :param task_id: The task's id.
    :type task_id: str
    :param revision: The tasks's revision number.
    :returns: Request
    '''

    url = "{}/tasks/{}".format(API_URL, task_id)
    body = {"revision": revision}
    return Request("DELETE", url, data=body)


def get_list(list_id):
    '''Get all information for one list.

    :param list_id: The list's ID.
    :returns: Request
    '''

    return Request("GET", "{}/lists/{}".format(API_URL, list_id))


def get_lists():
    '''Get all of the task lists

    :returns: Request
    '''

    return Request("GET", "{}/lists".format(API_URL))


def add_list(list_name):
    '''Create a new task list.

    :param list_name: The name of the new list.
    :type list_name: str
    :returns: Request
    '''

    body = {"title": list_name}
    return Request("POST", "{}/lists".format(API_URL), data=body)


def delete_list(list_id, revision):
    '''Delete a list and all of its contents.

    :param list_id: The id of the list to delete.
    :type list_id: str
    :param revision: The tasks's revision number.
    :returns: Request
    '''

    url = "{}/lists{}".format(API_URL, list_id)
    body = {"revision": revision}
    return Request("DELETE", url, data=body)


def get_comments(task_id):
    '''Get all comments from the specified task.

    :param task_id: The ID of the task.
    :type task_id: str
    '''

    url = "{}/task_comments".format(API_URL)
    body = {"task_id": task_id}
    return Request("GET", url, data=body)


def get_comment(comment_id):
    '''Get all information about a single comment.

    :param comment_id: The comment's ID.
    :returns: Request
    '''

    return Request("GET", "{}/task_comments/{}".format(API_URL, comment_id))


def add_comment(title, task_id):
    '''Add a comment to a task. I'm not sure if this works with batch

    :param title: The comment name/title.
    :param task_id: The ID of the task you're commenting on.
    :type title: str
    :type task_id: str
    :returns: Request
    '''

    url = "{}/task_comments".format(API_URL, task_id)
    body = {"task_id": task_id, "text": title}
    return Request("POST", url, data=body)


def get_reminders(task_id):
    '''Get a list of reminders for a task.

    :param task_id: The task's ID.
    :returns: Request
    '''

    body = {"task_id": task_id}
    return Request("GET", "{}/reminders".format(API_URL), data=body)


def set_reminder_for_task(task_id, date):
    '''Add a reminder for a task.

    :param task_id: The id of the task.
    :type task_id: str
    :param date: The reminder date/time in ISO format.
    :type date: str
    :returns: Request
    '''

    body = {"task_id": task_id, "date": date}  # date is in ISO date format
    return Request("POST", "{}/reminders".format(API_URL), data=body)


def get_memberships():
    '''Get a list of all things shared with you.

    :returns: Request
    '''

    return Request("GET", "{}/memberships".format(API_URL))


def get_file(file_id):
    '''Get all information about a file given its ID.

    :param file_id: The file's ID.
    :returns: Request
    '''

    return Request("GET", "{}/files/{}".format(API_URL, file_id))


def get_files(task_id):
    '''Get a list of all files belonging to a task.

    :param task_id: The task's ID.
    :returns: Request
    '''

    body = {"task_id": task_id}
    return Request("GET", "{}/files".format(API_URL), data=body)


def add_file(task_id):
    '''Add an empty file to a task.

    Note that this will give you an S3 url where you upload the file to.

    :param task_id: The task's ID.
    :returns: Request
    '''

    body = {"upload_id": 0, "task_id": task_id}
    return Request("POST", "{}/files".format(API_URL), data=body)


def delete_file(file_id, revision):
    '''Delete a file.

    :param file_id: The file's ID.
    :param revision: The file's revision number.
    :returns: Request
    '''

    body = {"id": file_id, "revision": revision}
    return Request("DELETE", "{}/files/{}".format(API_URL, file_id),
                   data=body)
