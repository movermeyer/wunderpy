/me/lists
=========

Make or read lists.

GET
---
Get all lists.

Example Response
""""""""""""""""
::

    [
       {
          "title":"Wishlist",
          "created_at":"2013-03-02T22:32:48Z",
          "updated_at":"2013-03-02T22:58:00Z",
          "version":2,
          "local_identifier":"localId:repopulated:owner:List:wish list",
          "position":5.0,
          "type":"List",
          "id":"id",
          "owner_id":"owner"
       },
       {
          "title":"Private",
          "created_at":"2013-03-02T22:32:48Z",
          "updated_at":"2013-03-02T22:32:48Z",
          "version":1,
          "local_identifier":"localId:repopulated:owner:List:private",
          "position":0.99999,
          "type":"List",
          "id":"id",
          "owner_id":"owner"
       },
       {
          "title":"Work",
          "created_at":"2013-03-02T22:32:48Z",
          "updated_at":"2013-03-02T22:32:48Z",
          "version":1,
          "local_identifier":"localId:repopulated:owner:List:work",
          "position":1.99999,
          "type":"List",
          "id":"id",
          "owner_id":"owner"
       },
       {
          "title":"Shopping",
          "created_at":"2013-03-02T22:32:48Z",
          "updated_at":"2013-03-02T22:32:48Z",
          "version":1,
          "local_identifier":"localId:repopulated:owner:List:shopping",
          "position":2.99996,
          "type":"List",
          "id":"id",
          "owner_id":"owner"
       },
       {
          "title":"test",
          "created_at":"2013-03-03T19:18:21Z",
          "updated_at":"2013-03-03T19:18:21Z",
          "version":1,
          "local_identifier":null,
          "position":0.0,
          "type":"List",
          "id":"id",
          "owner_id":"owner"
       }
    ]


POST
----
Create a new list.

Required Parameters
"""""""""""""""""""
:title: The list's name.

Example Response
""""""""""""""""
::

    {
       "version":1,
       "local_identifier":null,
       "title":"test",
       "position":0.0,
       "created_at":"2013-03-03T19:18:21Z",
       "owner_id":"id",
       "type":"List",
       "updated_at":"2013-03-03T19:18:21Z",
       "id":"id"
    }
