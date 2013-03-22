/<list_id>/shares
=================

POST
----

Share the list with another user.

Required Parameters
"""""""""""""""""""
:recipient: a dictionary like this: {"email": "email@place.com"}

Example Response
""""""""""""""""
::

    {
       "sender":{
          "email":"email@place.com",
          "id":"user_id",
          "avatar":null,
          "name":"Your Name"
       },
       "accepted_at":null,
       "resource_id":"list_id",
       "recipient":{
          "username":null,
          "provider_id":"email",
          "id":"recipient_id",
          "provider_type":"email"
       },
       "created_at":"2013-03-22T04:02:26Z",
       "updated_at":"2013-03-22T04:02:26Z",
       "resource_title":"Title",
       "local_identifier":null,
       "minisite_url":"https://www.wunderlist.com/#/shared/share_id/another_id",
       "type":"Share",
       "id":"share_id",
       "resource_type":"List"
    }
