#!/usr/bin/env python
"""pydstat main library.

Source:: https://github.com/ampledata/pydstat
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2011 Splunk, Inc.'
__license__ = 'Apache License, Version 2.0'


import os
import logging
import logging.handlers
import shlex
import subprocess


IGNORED_FIELDS = ('Time', 'PID', '%guest', 'CPU', 'Command')
HELP = 'https://github.com/ampledata/pydstat'


class PydStatError(StandardError):
    """Placeholder Exception for pydstat."""
    pass


class PydStat(object):
    """PydStat."""

    def __init__(self, pidstat=None, log_dest=None):
        self.log_dest = None
        self.pidstat = None
        self.stats = None
        self.logger = None
        self.stat_lines = None

        self._set_defaults(pidstat, log_dest)
        self._setup_logging()

    def _set_defaults(self, pidstat, log_dest):
        if pidstat is None:
            pidstat = '/usr/bin/pidstat'

        if os.path.exists(pidstat):
            self.pidstat = pidstat
        else:
            raise PydStatError(
                'pidstat does not exist at %s, cannot continue.' % pidstat)

        if log_dest is None or log_dest is '/dev/log':
            if os.path.exists('/dev/log'):
                self.log_dest = '/dev/log'
            else:
                self.log_dest = ('localhost', 514)
        elif log_dest is not None:
            self.log_dest = log_dest

    def _setup_logging(self):
        base_logger = logging.getLogger('pydstat')
        base_logger.setLevel(logging.DEBUG)

        syslog_logger = logging.handlers.SysLogHandler(self.log_dest, 'local5')
        syslog_logger_formatter = logging.Formatter(
            'pydstat: %(message)s')
        syslog_logger.setFormatter(syslog_logger_formatter)

        base_logger.addHandler(syslog_logger)
        self.logger = logging.LoggerAdapter(base_logger, {'help': HELP})

    def get_stats(self, pid='ALL'):
        """Call pidstat for the specified pid and return its output.

        @param pid: Pid to lookup. Default = 'ALL'
        @type pid: string

        @return: Output from subprocess.Popen() as a string split into a list.
        @rtype: list
        """
        devnullr = open('/dev/null', 'r')
        devnullw = open('/dev/null', 'w')

        pidstat = shlex.split(
            ' '.join([self.pidstat, '-druh', '-p', str(pid)]))

        proc = subprocess.Popen(
            pidstat,
            stdin=devnullr,
            stderr=devnullw,
            stdout=subprocess.PIPE)

        stdoutdata, _ = proc.communicate()

        self.stat_lines = stdoutdata.split('\n')

    def parse_stats(self):
        """Groks the output from pidstat.
        Also fixes weird field names: %, /s, etc
        """
        values = []
        for stat in self.stat_lines:
            if stat.startswith('#'):
                fixed_stat = stat.replace('%', 'pct_').replace('/', '')
                fields = fixed_stat.split()[1:]
            elif stat.startswith(' '):
                values.append(stat.split())

        # Make list of dicts with values for each PID.
        # e.g. [{'cmd': 'httpd', 'pct_CPU': '50'}]
        self.stats = [dict(zip(fields, v)) for v in values]

    def log_stats(self):
        """Logs stats to syslog."""
        for stat in self.stats:
            stat['cmdline'] = self.get_cmdline(stat['PID'])
            log = ['='.join([k, stat[k]]) for k in stat]
            self.logger.debug(' '.join(log))

    @classmethod
    def get_cmdline(cls, pid):
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
