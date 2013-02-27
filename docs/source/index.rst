.. Wunderpy documentation master file, created by
   sphinx-quickstart on Mon Feb 25 20:59:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


What is Wunderpy?
=================

Wunderpy is a python package that aims to provide access to the `Wunderlist <https://www.wunderlist.com>`_ API.

As of this writing (2/13), Wunderlist doesn't have a public, documented API. This means that I've had to rely exclusively on reverse engineering the Wunderlist application (OS X Desktop) to figure out how to use it. Thus, it's quite possible that things will change unexpectedly and break everything.

That being said, wunderpy does some things differently from the official client. Presently, it doesn't send any client information (OS version, client version, etc) in the HTTP headers, and it doesn't use the /batch functionality of the API, which allows you to perform multiple calls while only sending one request. Currently wunderpy *cannot* login with OAuth.

Wunderpy provides two things: an interface to the Wunderlist API itself, and a very basic client class wrapped around it.

Contents
========

.. toctree::
   :maxdepth: 1

   examples
   wunderlist
   _api
   wunderlist_api/index 

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
