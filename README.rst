A Pythonic wrapper for `pidstat`_.

Collects and returns process stats in Cloudkick and syslog formats.

. `pidstat`: http://manpages.ubuntu.com/manpages/lucid/en/man1/pidstat.1.html

Usage
=====
There are at least three possible ways to use this script.

#. Add as custom plugin for your Cloudkick agent (TK).
#. Create crontab to run periodically::

    */5 * * * * /usr/local/bin/pydstat.py

#. Add as Splunk scripted input (TK).


Author
======
Greg Albrecht <gba@splunk.com>

Copyright
=========
Copyright 2011 Splunk, Inc.

License
=======
Apache License 2.0
