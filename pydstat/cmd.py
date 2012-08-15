#!/usr/bin/env python
"""Collect and return process stats in Cloudkick and syslog formats.

A Pythonic wrapper for pidstat:
http://manpages.ubuntu.com/manpages/lucid/en/man1/pidstat.1.html

Usage
=====
  There are at least three possible ways to use this script.

    1. Add as custom plugin for your Cloudkick agent (TK).
    2. Create crontab to run periodically:
      */5 * * * * /usr/local/bin/pydstat.py
    3. Add as Splunk scripted input (TK).

License
=======
  Copyright 2011 Splunk, Inc.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2011 Splunk, Inc.'
__license__ = 'Apache License, Version 2.0'
__help__ = 'https://github.com/ampledata/pydstat'


import os
import logging
import logging.handlers
import sys
import subprocess


class PydStatError(StandardError):
    """Placeholder Exception for pydstat."""
    pass


class PydStat(object):

    IGNORED_FIELDS = ('Time', 'PID', '%guest', 'CPU', 'Command')

    def __init__(self):
        self.logger = self._setup_logging()

    def _setup_logging(self):
        if os.path.exists('/dev/log'):
            log_dest = '/dev/log'  # Log Locally
        else:
            log_dest = ('localhost', 514)

        base_logger = logging.getLogger('ck')
        base_logger.setLevel(logging.DEBUG)

        syslog_logger = logging.handlers.SysLogHandler(log_dest, 'local5')
        syslog_logger_formatter = logging.Formatter(
            'pydstat: %(message)s # Help: %(help)s')
        syslog_logger.setFormatter(syslog_logger_formatter)

        base_logger.addHandler(syslog_logger)
        return logging.LoggerAdapter(base_logger, {'help': __help__})


    def get_stats(self, pid=None):
        """Call pidstat for the specified pid and return its output.

        Most of this is inherited from _pidstatMetrics.

        @param pid: Pid to lookup.
        @type pid: string

        @return: Output from subprocess.Popen() as a string split into a list.
        @rtype: list
        """
        devnullr = open('/dev/null', 'r')
        devnullw = open('/dev/null', 'w')

        pidstat = '/usr/bin/pidstat'
        if not os.path.exists(pidstat):
            raise PydStatError(
                'pidstat does not exist at %s, cannot continue.' % pidstat)

        pidstat = ' '.join((pidstat, '-druh'))
        if pid is not None:
            pidstat = ' '.join((pidstat, '-p', pid))

        proc = subprocess.Popen(
            pidstat.split(),
            stdin=devnullr,
            stderr=devnullw,
            stdout=subprocess.PIPE)

        stdoutdata, _ = proc.communicate()
        return stdoutdata.split('\n')


    def get_cmdline(self, pid):
        """Get cmdline for given PID.

        @param pid: Pid to lookup.
        @type pid: string

        @return: Contents of /proc/$pid/cmdline.
        @rtype: str
        """
        cmdline = ''
        cmdline_file = os.path.join(os.path.sep, 'proc', pid, 'cmdline')

        if os.path.exists(cmdline_file):
            with open(cmdline_file, 'r') as cmdline_fd:
                cmdline = cmdline_fd.read()

        # cmdline is NULL terminated, lets replace those with spaces.
        return "'%s'" % cmdline.rstrip('\x00').replace('\x00', ' ')


    def parse_stats(self, stats):
        """Groks the output from pidstat. Also fixes weird field names: %, /s, etc

        @param stats: Output of pidstat as a list
        @type stats: list

        @return: List of stats for each PID specified (or all pids).
        @rtype: list
        """
        values = []
        for stat in stats:
            if stat.startswith('#'):
                fixed_stat = stat.replace('%', 'pct_').replace('/', '')
                fields = fixed_stat.split()[1:]
            elif stat.startswith(' '):
                values.append(stat.split())
        # Make list of dicts with values for each PID.
        # e.g. [{'cmd': 'httpd', 'pct_CPU': '50'}]
        return [dict(zip(fields, v)) for v in values]


    def ck_print_stats(self, stats):
        """Detects a metric's type (int or float) and print it in Cloudkick format.

        @param stats: A string list of metrics as returned by get_stats()
        @type stats: string
        """
        for k in stats:
            if not k in IGNORED_FIELDS:
                try:
                    int(stats[k])
                    vtype = 'int'
                except ValueError:
                    vtype = 'float'
                print ' '.join(['metric', k, vtype, stats[k]])


    def log_stats(self, stats):
        """Logs stats to syslog.
        Replace PyDict/JSON style string with k=v string.

        @param stats: A list of metrics as returned by get_stats()
        @type stats: list
        """
        stats['cmdline'] = get_cmdline(stats['PID'])
        log = ['%s=%s' % (k, stats[k]) for k in stats]
        LOGGER.debug(' '.join(log))


    def main():
        """Main program loop, parses args, calls stuff."""

        # If you don't specify a PID we'll stat them all.
        # If you specify a PID, we'll just stat that one.
        if len(sys.argv) != 2:
            lines = get_stats()
        elif sys.argv[1] == 'test-single':
            lines = TEST_SINGLE.splitlines()
        elif sys.argv[1] == 'test-all':
            lines = TEST_ALL.splitlines()
        else:
            lines = get_stats(sys.argv[1])

        stats = parse_stats(lines)

        # If there's only one item we're in single PID mode, which is reverse-
        # compatible with the format Cloudkick expects.
        if len(stats) == 1:
            ck_print_stats(stats[0])

        # Now syslog everything.
        for stat in stats:
            log_stats(stat)
