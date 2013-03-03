/me/tasks
=========

Create or read tasks.

GET
---
Read all tasks.

Example Response
""""""""""""""""
::

    [
       {
          "recurrence_count":0,
          "updated_at":"2013-03-03T19:36:28Z",
          "assignee_id":null,
          "completed_at":null,
          "updated_by_id":"owner",
          "recurrence_type":null,
          "deleted_at":null,
          "id":"id",
          "user_id":"owner",
          "title":"test",
          "recurring_parent_id":null,
          "note":null,
          "parent_id":null,
          "version":1,
          "list_id":"inbox",
          "type":"Task",
          "owner_id":"owner",
          "due_date":"2013-03-03",
          "created_by_id":"owner",
          "created_at":"2013-03-03T19:36:28Z",
          "local_identifier":null,
          "position":0.0,
          "starred":true
       },
       {
          "recurrence_count":0,
          "updated_at":"2013-02-26T06:00:28Z",
          "assignee_id":null,
          "completed_at":null,
          "updated_by_id":"id",
          "recurrence_type":null,
          "deleted_at":null,
          "id":"id",
          "user_id":"id",
          "title":"test",
          "recurring_parent_id":null,
          "note":null,
          "parent_id":null,
          "version":2,
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
    ]

POST
----
Create a task.

Parameters
""""""""""
:list_id: The ID of the list to put this task in. "inbox" for inbox list.
:title: The task name.
:starred: (optional) Whether the task should be starred or not. 0 or 1
:due_date: (optional) The date the task should be due on. The date is in ISO format. Example: 2012-12-30T06:00:28Z

Example Response
""""""""""""""""
::

    {
       "recurrence_count":0,
       "updated_at":"2013-03-03T19:36:28Z",
       "assignee_id":null,
       "completed_at":null,
       "updated_by_id":"id",
       "recurrence_type":null,
       "deleted_at":null,
       "id":"id",
       "user_id":"id",
       "title":"test",
       "recurring_parent_id":null,
       "note":null,
       "parent_id":null,
       "version":1,
       "list_id":"inbox",
       "type":"Task",
       "owner_id":"id",
       "due_date":"2013-03-03",
       "created_by_id":"id",
       "created_at":"2013-03-03T19:36:28Z",
       "local_identifier":null,
       "position":0.0,
       "starred":true
    }