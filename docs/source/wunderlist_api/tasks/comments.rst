/tasks/<task_id>/messages
=========================

Get or add comments.

As of this writing, these requests must go to the https://comments.wunderlist.com endpoint. Becuase of this, comment requests can't be used with batch.

GET
---

Get all comments for a task.

Example Response
""""""""""""""""
::

	[
	  {
	    "channel_type": "tasks",
	    "channel_id": "id",
	    "local_created_at": "2013-09-29T05:50:35.000Z",
	    "author": {
	      "id": "id",
	      "name": "name",
	      "avatar": "URL_omitted"
	    },
	    "text": "this is a comment",
	    "created_at": "2013-09-29T05:50:35Z",
	    "type": "Message",
	    "updated_at": "2013-09-29T05:50:35Z",
	    "id": comment_id
	  }
	]

POST
----

Add a comment to a task.

Parameters
""""""""""
:channel_id: The task's ID.
:channel_type: This should always be "tasks"
:text: The actual comment. In this example it's "this is a comment"

Example Response
""""""""""""""""
::

	{
	  "channel_type": "tasks",
	  "channel_id": "id",
	  "local_created_at": "2013-09-29T05:50:35.032Z",
	  "author": {
	    "id": "id",
	    "name": "name",
	    "avatar": "URL_omitted"
	  },
	  "text": "this is a comment",
	  "created_at": "2013-09-29T05:50:35Z",
	  "type": "Message",
	  "updated_at": "2013-09-29T05:50:35Z",
	  "id": comment_id
	}
