wunderpy
========

The goal of this project is to make [Wunderlist's](https://wunderlist.com) private and undocumented API less private and better documented, while also providing a python client implementation. I've explained how I figured out the API in a blog post [here](http://bsmt.me/blog/2013/03/02/reverse-engineering-the-wunderlist-api/), in case anyone is curious or wants to contribute.

You can read the documentation at [readthedocs.](https://wunderpy.readthedocs.org/en/latest/)

Building the Docs
-----------------

Chances are, you're looking for information on how to use the API. I'm in the process of documenting everything in wunderpy. Information on the API, as well as the classes provided by wunderpy are documented with sphinx.

To generate the documentation:

    cd docs
    make html # other options are available
    # look in the docs/build/html dir for the documentation
