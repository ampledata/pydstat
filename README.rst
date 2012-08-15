A Pythonic wrapper for `pidstat`_.

Collects and returns process stats in syslog format.

.. _pidstat: http://manpages.ubuntu.com/manpages/lucid/en/man1/pidstat.1.html

.. image:: https://secure.travis-ci.org/ampledata/pydstat.png
        :target: https://secure.travis-ci.org/ampledata/pydstat

Usage
=====
#. Create crontab to run periodically::

    */5 * * * * /usr/local/bin/pydstat

#. Use `Splunk`_ to collect logs.

.. _Splunk: http://www.splunk.com/

Source
======
https://github.com/ampledata/pydstat

Author
======
Greg Albrecht <gba@splunk.com>

Copyright
=========
Copyright 2011 Splunk, Inc.

License
=======
Apache License 2.0
