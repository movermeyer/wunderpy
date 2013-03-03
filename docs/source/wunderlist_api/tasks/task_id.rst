/me/<task_id>
=============

Modify or delete tasks.

PUT
---
Modify a task.

Parameters
""""""""""
:task_id: Passed in the URL.
:note: The new note for the task.
:due_date: The new due date for the task (ISO format as usual).
:recurrence_count: Not positive.

Example Response
""""""""""""""""
::

    {
       "recurrence_count":0,
       "updated_at":"2013-03-03T19:44:48Z",
       "assignee_id":null,
       "completed_at":null,
       "updated_by_id":"owner",
       "recurrence_type":null,
       "deleted_at":null,
       "id":"id",
       "user_id":"owner",
       "title":"test",
       "recurring_parent_id":null,
       "note":"lawlrus",
       "parent_id":null,
       "version":3,
       "list_id":"inbox",
       "type":"Task",
       "owner_id":"owner",
       "due_date":null,
       "created_by_id":"owner",
       "created_at":"2013-02-26T05:59:58Z",
       "local_identifier":"localId:Mac:owner:Task:GUID",
       "position":0.0001,
       "starred":false
    }

DELETE
------
Delete a task.

Required Parameters
"""""""""""""""""""
:task_id: Passed in the URL.
