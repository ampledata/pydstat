#!/usr/bin/env python
"""Collect and return process stats in Cloudkick and syslog formats.

A Pythonic wrapper for pidstat:
http://manpages.ubuntu.com/manpages/lucid/en/man1/pidstat.1.html

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
__help__ = 'https://ampledata.github.com/pydstat'


import os
import logging
import logging.handlers
import sys
import subprocess


def setup_logging():
    """Sets up logging for pydstat."""
    base_logger = logging.getLogger('ck')
    base_logger.setLevel(logging.DEBUG)
    if os.path.exists('/dev/log'):
        log_dest = '/dev/log'  # Log Locally
    else:
        log_dest = ('localhost', 514)
    slh = logging.handlers.SysLogHandler(log_dest, 'local5')
    slh.setLevel(logging.DEBUG)
    slh_formatter = logging.Formatter('pydstat: %(message)s # Help: %(help)s')
    slh.setFormatter(slh_formatter)
    base_logger.addHandler(slh)
    # Stream (console) for testing 'log' output w/o syslog.
    #clh = logging.StreamHandler()
    #base_logger.addHandler(clh)
    return logging.LoggerAdapter(base_logger, {'help': __help__})

LOGGER = setup_logging()

IGNORED_FIELDS = ('Time', 'PID', '%guest', 'CPU', 'Command')

# pylint: disable=C0301
TEST_SINGLE = """Linux 2.6.32-312-ec2 (orchestration-i-78061518.prod)    12/06/2011      _x86_64_        (2 CPU)

#      Time       PID    %usr %system  %guest    %CPU   CPU  minflt/s  majflt/s     VSZ    RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s  Command
 1323215317     22432 2101308837.50 1109883172442.43    0.00 1111984481279.93     0      1.11      0.00  158392  67444   0.86      0.00      0.00      0.00  chef-client
"""

TEST_ALL = """Linux 2.6.32-312-ec2 (orchestration-i-78061518.prod)    12/06/2011      _x86_64_        (2 CPU)

#      Time       PID    %usr %system  %guest    %CPU   CPU  minflt/s  majflt/s     VSZ    RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s  Command
 1323224972      2462    0.00    0.00    0.00    0.00     1      0.00      0.00   25808   1568   0.02      0.00      0.03      0.00  ntpd
 1323224972      5689 85268448194.21 4348690857956.36    0.00   51.60     0     23.52      0.00  184180  19864   0.25      0.00      0.09      0.00  cloudkick-agent
 1323224972      6157    0.00    0.00    0.00    0.00     1      0.00      0.00   11936    612   0.01      0.00      0.00      0.00  ssh-agent
 """


class PydstatError(StandardError):
    """Placeholder Exception for pydstat."""
    pass


def get_stats(pid=None):
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
        raise PydstatError(
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


def parse_stats(stats):
    """Groks the output from pidstat.

    @param stats: Output of pidstat as a list
    @type stats: list

    @return: List of stats for each PID specified (or all pids).
    @rtype: list
    """
    values = []
    for stat in stats:
        if stat.startswith('#'):
            fields = stat.split()[1:]
        elif stat.startswith(' '):
            values.append(stat.split())
    # Make list of dicts with values for each PID.
    # e.g. [{'cmd': 'httpd', '%CPU': '50'}]
    return [dict(zip(fields, v)) for v in values]


def ck_print_stats(stats):
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


def log_stats(stats):
    """Logs stats to syslog.

    Replace PyDict/JSON style string with k=v string. Also replace weird field
    names, e.g. '%CPU', 'kb/s'.

    @param stats: A list of metrics as returned by get_stats()
    @type stats: list
    """
    log = ['%s=%s' % (k, stats[k]) for k in stats]
    LOGGER.debug(' '.join(log).replace('%', 'pct_').replace('/s', 's'))


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


if __name__ == '__main__':
    main()
