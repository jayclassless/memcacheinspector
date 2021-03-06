=================
memcacheinspector
=================
----------------------------------------------------
Memcached Inspection Module and Command-Line Utility
----------------------------------------------------

Introduction
============

This package includes two things:

- A `Python`_ module for extracting keys from `Memcached`_ servers.
- A command-line utility for exploring, searching, and updating `Memcached`_ items.

This utility makes use of the `Memcached`_ status "features" discussed in the `SensePost Blog`_.


Installation
============

Using `pip`_ (recommended)::

    $ pip install memcacheinspector

Or, using easy_install::

    $ easy_install memcacheinspector

Or, you can download the source and install it by hand::

    $ python setup.py install

Installing the package installs both the memcacheinspector python module as well as the mcinspect command-line utility.


Requirements
============

- Python 2.5+
- The `python-memcached`_ module.


Usage
=====

::

    Usage: mcinspect [options] <action> [<arguments>]

    Actions:
      list                     Lists all items stored in the server(s).
      dump                     Dumps all items (including values) stored in the
                               server(s).
      grep <pattern>           Dumps all items (including values) whose key or value
                               matches the specified search pattern.
      get <key> [<key> ...]    Retrieves the items with the specified key(s).
      set <key> <value>        Sets the item with the specified key and value.
      incr key                 Increments the value of the items with the specified
                               key(s).
      decr key                 Decrements the value of the items with the specified
                               key(s).
      delete <key> [<key> ...] Deletes the items with the specified key(s).
      flush                    Expires all items in the server(s).
      stats                    Retrieves statistics from the server(s).

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -s SERVER, --server=SERVER
                            Specifies a server to connect to. Can be used multiple
                            times. Defaults to '127.0.0.1:11211'.
      -z MAX_VALUE_SIZE, --max-value-size=MAX_VALUE_SIZE
                            The maximum size (in bytes) of a value can be when
                            performing a list or dump action. Zero or lower is
                            interpreted as no limit. Defaults to 0.
      -d DELTA, --delta=DELTA
                            The amount to change the value when using the incr or
                            decr actions. Defaults to 1.
      -i, --ignore-case     Ignore case distinctions in both the pattern and the
                            items during the grep action.
      -v, --invert-match    Inverts the sense of matching, to select non-matching
                            items during the grep action.

    Output Format:
      list:
        <server connection string>|<expiration date>|<size in bytes>|<key>

      dump, grep:
        <server connection string>|<expiration date>|<size in bytes>|<key>
        <value>

      get, set, incr, decr:
        <server connection string>|<key>
        <value>

      delete:
        <server connection string>|<key>

      flush:
        <server connection string>

      stats:
        <server connection string>|<statistic key>|<value>


License
=======

memcacheinspector is released under the `MIT License`_. See the LICENSE file for full text of the license.


Reference
=========

_`Home`: http://bitbucket.org/jayclassless/memcacheinspector/

_`Package Index`: http://pypi.python.org/pypi/memcacheinspector/

_`Python`: http://www.python.org/

_`Memcached`: http://memcached.org/

_`python-memcached`: http://www.tummy.com/Community/software/python-memcached/

_`pip`: http://pip.openplans.org/

_`SensePost Blog`: http://www.sensepost.com/blog/4873.html

_`MIT License`: http://www.opensource.org/licenses/mit-license.php
