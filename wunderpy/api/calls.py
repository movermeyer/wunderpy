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


### Avatar
def get_avatar(user_id):
    '''Get the avatar for a user.

    :param user_id: The user's ID.
    :returns: Request
    '''

    return Request("GET". "{}/avatar".format(API_URL))


### File
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


### File preview
def get_preview(file_id):
    '''Request a thumbnail for an image.

    :param file_id: The file/image's ID.
    :returns: Request
    '''

    body = {"file_id": file_id}
    return Request("GET", "{}/previews".format(API_URL), data=body)


### List
def get_lists():
    '''Get all of the task lists

    :returns: Request
    '''

    return Request("GET", "{}/lists".format(API_URL))


def get_list(list_id):
    '''Get all information for one list.

    :param list_id: The list's ID.
    :returns: Request
    '''

    return Request("GET", "{}/lists/{}".format(API_URL, list_id))


def get_number_of_tasks(list_id):
    '''Get the number of tasks in a list.

    :param list_id: The list's ID.
    :returns: Request
    '''

    return Request("GET", "{}/lists/tasks_count".format(API_URL),
                   data={"list_id": list_id})


def add_list(list_name):
    '''Create a new task list.

    :param list_name: The name of the new list.
    :type list_name: str
    :returns: Request
    '''

    body = {"title": list_name}
    return Request("POST", "{}/lists".format(API_URL), data=body)


def set_list_title(list_id, title, revision):
    '''Change a list's title.

    :param list_id: The list's ID.
    :param title: The new title.
    :param revision: The list's revision number.
    :returns: Request
    '''

    body = {"revision": revision, "title": title}
    return Request("PATCH", "{}/lists/{}".format(API_URL, list_id),
                   data=body)


def set_list_public(list_id, revision, public=True):
    '''Set whether a list should be publicly visible.

    :param list_id: The list's ID.
    :param revision: The list's revision number.
    :param public: Will it be public?
    :returns: Request
    '''

    body = {"revision": revision, "public": public}
    return Request("PATCH", "{}/lists/{}".format(API_URL, list_id),
                   data=body)


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


### Membership
def get_memberships():
    '''Get a list of all things shared with you.

    :returns: Request
    '''

    return Request("GET", "{}/memberships".format(API_URL))


def add_to_list(user_id, list_id, muted=False):
    '''Share a list with a user.

    :param user_id: The user's ID.
    :param list_id: The list's ID.
    :param muted: Can they make changes?
    :returns: Request
    '''

    body = {"user_id": user_id, "list_id": list_id, "muted": muted}
    return Request("POST", "{}/memberships".format(API_URL), data=body)


def accept_membership(membership_id, revision, muted=False):
    '''Accept a membership request?

    :param membership_id: The membership request's ID.
    :param revision: The membership request's revision number.
    :param muted: ?
    :returns: Request
    '''

    body = {"revision": revision, "state": "accepted", "muted": muted}
    re = Request("PATCH", "{}/memberships/{}".format(API_URL, membership_id),
                 data=body)
    return re


def revoke_membership(membership_id, revision):
    '''Remove a member from a list.

    :param membership_id: The membership's ID.
    :param revision: The membership entity revision.
    :returns: Request
    '''

    body = {"revision": revision}
    re = Request("DELETE", "{}/memberships/{}".format(API_URL, membership_id),
                 data=body)


def reject_invitation(membership_id, revision):
    '''Reject an invite to a list.

    :param membership_id: The membership invitation's ID.
    :param revision: The membership invitation's revision number.
    :returns: Request
    '''

    body = {"revision": revision}
    re = Request("DELETE", "{}/memberships/{}".format(API_URL, membership_id),
                 data=body)
    return re


### Note
def get_notes(task_id):
    '''Get the notes for a task.

    :param task_id: The task's ID.
    :returns: Request
    '''

    return Request("GET", "{}/notes".format(API_URL),
                   data={"task_id": task_id})


def get_note(note_id):
    '''Get all data for a single note.

    :param note_id: The note's ID.
    :returns: Request
    '''

    return Request("GET", "{}/notes/{}".format(API_URL, note_id))


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


def update_note(note_id, new_content, revision):
    '''Modify an existing note.

    :param note_id: The note's ID.
    :param new_content: The new note content.
    :param revision: The note's revision number.
    :returns: Request.
    '''

    body = {"content": new_content, "revision": revision}
    return Request("PATCH", "{}/notes/{}".format(API_URL, note_id),
                   data=body)


def delete_note(note_id):
    '''Delete a note.

    :param note_id: The note's ID.
    :returns: Request
    '''

    return Request("DELETE". "{}/notes/{}".format(API_URL, note_id))


### Positions
### I don't really care about this stuff, but I'll put it in anyways.
def get_list_positions():
    '''Get the order of all lists..

    :returns: Request
    '''

    return Request("GET", "{}/list_positions".format(API_URL))


def get_list_position(list_id):
    '''Get the position of a single list.

    :param list_id: The list's ID.
    :returns: Request
    '''

    return Request("GET", "{}/list_positions/{}".format(API_URL, list_id))


def update_positions():
    pass


def get_task_positions(list_id):
    '''Get the positions of the tasks in a list.

    :param list_id: The list's ID.
    :returns: Request
    '''

    return Request("GET", "{}/task_positions".format(API_URL),
                   data={"list_id": list_id})


def get_task_position(task_id):
    '''Get the position of a single task within its list.

    :param task_id: The task's ID.
    :returns: Request
    '''

    return Request("GET", "{}/task_positions/{}".format(API_URL, task_id))


def update_task_positions():
    pass


def get_subtask_positions(task_id):
    '''Get the positions of the subtasks in a task.

    :param task_id: The task's ID.
    :returns: Request
    '''

    return Request("GET", "{}/subtask_positions".format(API_URL),
                   data={"task_id": task_id})


def get_subtask_position(task_id):
    pass


def update_subtask_positions(task_id, subtasks, revision):
    '''Set the positions of subtasks within a task.

    :param task_id: The task's ID.
    :param subtasks: A list of subtask IDs in the order you want.
    :type subtasks: list
    :param revision: The task's revision number.
    :returns: Request
    '''

    re = Request("PATCH", "{}/subtask_positions/{}".format(API_URL, task_id),
                 data={"values": subtasks, "revision": revision})
    return re


### Reminder
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


def update_reminder(reminder_id, date, revision):
    '''Update the date on a reminder.

    :param reminder_id: The reminder's ID.
    :param date: The new reminder date/time in ISO format.
    :type date: str
    :param revision: The reminder's revision number.
    :returns: Request
    '''

    return Request("PATCH", "{}/reminders/{}".format(API_URL, reminder_id),
                   data={"date": date, "revision": revision})


def delete_reminder(reminder_id, revision):
    '''Delete a reminder.

    :param reminder_id: The reminder's ID.
    :param revision: The reminder's revision number.
    :returns: Request
    '''

    return Request("DELETE", "{}/reminders/{}".format(API_URL, reminder_id),
                   data={"id": reminder_id, "revision": revision})


### Subtask
def get_subtasks(task_id, completed=False):
    '''Get all subtasks for a task.

    :param task_id: The task's ID.
    :param completed: Return completed subtasks?
    :returns: Request
    '''

    return Request("GET", "{}/subtasks".format(API_URL),
                   data={"task_id": task_id, "completed": completed})


def get_subtask(subtask_id):
    '''Get all data for a single subtask.

    :param subtask_id: The subtask's ID.
    :returns: Request
    '''

    return Request("GET", "{}/subtasks/{}".format(API_URL, subtask_id))


def add_subtask(task_id, title):
    '''Add a subtask to a task.

    :param task_id: The parent task's ID.
    :param title: The subtask's name.
    :returns: Request
    '''

    return Request("POST", "{}/subtasks".format(API_URL),
                   data={"task_id": task_id, "title": title,
                         "completed": False})


def update_subtask_title(subtask_id, new_title, revision):
    '''Change a subtask's title.

    :param subtask_id: The subtask's ID.
    :param new_title: The subtask's new name.
    :param revision: The subtask's revision number.
    :returns: Request
    '''

    return Request("PATCH", "{}/subtasks/{}".format(API_URL, subtask_id),
                   data={"revision": revision, "title": new_title})


def complete_subtask(subtask_id, revision, complete=True):
    '''Complete a subtask.

    :param subtask_id: The subtask's ID.
    :param revision: The subtask's revision number.
    :returns: Request
    '''

    return Request("PATCH", "{}/subtasks/{}".format(API_URL, subtask_id),
                   data={"completed": complete, "revision": revision})


def delete_subtask(subtask_id, revision):
    '''Delete a subtask.

    :param subtask_id: The subtask's ID.
    :param revision: The subtask's revision number.
    :returns: Request
    '''

    return Request("DELETE", "{}/subtasks/{}".format(API_URL, subtask_id))


### Task
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


def set_task_recurring(task_id, recurrence_type, recurrence_count, revision):
    '''Set a task to be recurring.

    :param task_id: The task's ID.
    :param recurrence_type: day, week, month, or year.
    :type recurrence_type: str
    :param recurrence_count: A number >= 1.
    :type recurrence_count: int
    :param revision: The task's revision number.
    :returns: Request
    '''

    url = "{}/tasks/{}".format(API_URL, task_id)
    body = {"recurrence_type": recurrence_type,
            "recurrence_count": recurrence_count,
            "revision": revision}
    return Request("PATCH", url, data=body)


def set_task_title(task_id, new_title, revision):
    '''Change a task's title.

    :param task_id: The task's ID.
    :param new_title: The new title for the task.
    :param revision: The task's revision number.
    :returns: Request
    '''

    url = "{}/tasks/{}".format(API_URL, task_id)
    return Request("PATCH", url, data={"title": title, "revision": revision})


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


### Task comment
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


### Upload
def create_upload(content_type, file_name, file_size):
    '''Create an upload object for a file.

    :param content_type: A MIME type for the data, I assume.
    :param file_name: The file's name.
    :param file_size: The size of the file, in bytes I think.
    :returns: Request
    '''

    body = {"content_type": content_type, "file_name": file_name,
            "file_size": file_size}
    return Request("POST", "{}/uploads".format(API_URL), data=body)


def finish_upload(upload_id):
    '''Tell the server you're done uploading.

    :param upload_id: The upload object's ID.
    :returns: Request
    '''

    return Request("PATCH", "{}/uploads/{}".format(API_URL, upload_id),
                   data={"state": "finished"})


### User
def get_user():
    '''Request for /user, which returns user information.

    :returns: Request
    '''

    return Request("GET", "{}/user".format(API_URL))
