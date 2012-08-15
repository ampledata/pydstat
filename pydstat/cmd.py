#!/usr/bin/env python
"""pydstat CLI Client.

Source:: https://github.com/ampledata/pydstat
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import sys

import pydstat


def main():
    """Main loop.

    If you don't specify a PID we'll stat them all.
    If you specify a PID, we'll just stat that one.
    """
    pyds = pydstat.PydStat()

    if len(sys.argv) != 2:
        pyds.get_stats()
    else:
        pyds.get_stats(sys.argv[1])

    pyds.parse_stats()
    pyds.log_stats()


if __name__ == '__main__':
    sys.exit(main())
