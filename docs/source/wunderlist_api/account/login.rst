/login
======

Log in to Wunderlist.

The token received will be used for every other request to authenticate yourself.
The key is "Authorization", and the value is "Bearer " + token.

POST
----
Params
""""""
:email: Your account's email.
:password: You account's password.

Example Response
""""""""""""""""
::

    {
       "product":"Product string",
       "name":"Your name",
       "settings":{
          "smartlist_visibility_week":"auto",
          "smartlist_visibility_today":"auto",
          "confirm_delete_entity":"true",
          "smartlist_visibility_starred":"auto",
          "print_completed_items":"false",
          "sound_notification_enabled":"true",
          "newsletter_subscription_enabled":"false",
          "account_locale":"en",
          "new_task_location":"bottom",
          "smartlist_visibility_all":"hidden",
          "smartlist_visibility_done":"hidden",
          "notifications_desktop_enabled":"true",
          "background":"wlbackground01",
          "sound_checkoff_enabled":"true",
          "notifications_email_enabled":"true",
          "use_badge_icon":"notifications"
       },
       "created_at":"2012-12-30T06:00:28Z",
       "updated_at":"2013-02-26T09:16:56Z",
       "email":"youremail@someplace.com",
       "token":"Your token",
       "avatar":null,
       "confirmation_state":"confirmed_email",
       "type":"User",
       "id":"Your id",
       "email_confirmed":true
    }
