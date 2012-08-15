#!/usr/bin/env python

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

