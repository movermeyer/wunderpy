wunderpy
========

|Build Status| |Version| |Downloads|

This here is a Wunderlist API wrapper for python. It was originally the only
publicly available client for their API, and somehow became popular...

You can read the documentation at `readthedocs.`_

Disclaimer
----------

In no way is this project near complete or perfect. There are a lot of
things that can be done better, especially design-wise, that I'm trying
to fix as I learn more. Things are liable to change or break
unexpectedly.

Example
-------

::

    from datetime import datetime
    from wunderpy import Wunderlist

    w = Wunderlist()
    w.login("username", "password")
    w.update_lists()  # you have to run this first, before you do anything else

    w.add_list("test")  # make a new list called "test"

    due = datetime.now().isoformat()
    w.add_task("test wunderpy", list_title="test", note="a note",
               due_date=due, starred=True)  # add a task to it
    w.complete_task("test wunderpy", "test")  # complete it
    w.delete_task("test wunderpy", "test")  # and delete it

    w.delete_list("test")  # and delete the list

Buildout
--------

To generate scripts for testing and documentation run buildout. For details
about buildout see http://www.buildout.org/en/latest/docs/index.html

::

    python bootstrap.py
    bin/buildout

Building the Docs
-----------------

Building the documentation can be done with the script bin/build_docs:

::

    bin/build_docs
    open docs/html/index.html

Running Tests
-------------

I'm working on writing tests for everything.

If you want to run said tests, make sure you have run the buildout. Once you have nose, all you have to do is run the tests.

::

    bin/test

By default, nose will not run any tests for the API calls, as they take around 30 seconds. If you want to run those tests, you can either store your email and password in
the WUNDERPY_EMAIL and WUNDERPY_PASSWORD env_vars, or you can install nose-testconfig and create an ini file like this:

::

    [login]
    email = test@email.web
    password = password

Then you can run nosetests with the --tc-file argument.

Contributing
------------

First off, I can't thank you enough. This is my first open source project that receives even a small amount of attention, so I'm a bit new to all of this. I don't have many guidelines, just make sure your code passes PEP8, and try to have pull requests merge to the develop branch. I like to follow something akin to the `gitflow`_ branching model, so merging to develop makes that a lot easier.

Changelog
---------

0.3.0
^^^^^

* added buildout to project

* Remove the Wunderlist CLI.

  * You can find a replacement `here`_

* Switch to the Wunderlist 3 API.

0.2.4
^^^^^

* Bugfixes

0.2.2
^^^^^

* Client

  * Add TaskList and Task classes
  * Add filtering methods
  * Add tests for new classes and most Wunderlist functionality

* CLI

  * Add --today and --week options
  * Only display incomplete tasks by default, add --show-complete option.


0.2.1
^^^^^
* Add a CLI interface
* Ensure session headers are included in all requests

License
-------

The MIT License (MIT)

Copyright (c) 2015 bsmt

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. _Wunderlist's: https://wunderlist.com
.. _readthedocs.: http://wunderpy.readthedocs.org/en/latest/

.. _here: https://github.com/bsmt/arbeit

.. |Build Status| image:: https://travis-ci.org/bsmt/wunderpy.png
   :target: https://travis-ci.org/bsmt/wunderpy
.. |Version| image:: https://pypip.in/v/wunderpy/badge.png
    :target: https://pypi.python.org/pypi/wunderpy
.. |Downloads| image:: https://pypip.in/d/wunderpy/badge.png
    :target: https://crate.io/packages/wunderpy/

.. _gitflow: http://nvie.com/posts/a-successful-git-branching-model/
