#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for pydstat parsing.

Source:: https://github.com/ampledata/pydstat
"""

import shlex
import subprocess
import unittest

from context import pydstat


class TestPydStat(unittest.TestCase):
    """Tests for pydstat."""

    def test_get_stats_one(self):
        pyds = pydstat.PydStat()
        pyds.get_stats()
        pyds.parse_stats()
        pyds.log_stats()

    def test_get_init_stats(self):
        pyds = pydstat.PydStat()
        pyds.get_stats(1)

    def test_get_cmdline(self):
        proc = subprocess.Popen(shlex.split('ps -ef'))
        pyds = pydstat.PydStat()
        pyds.get_stats(proc.pid)
        pyds.parse_stats()
        pyds.log_stats()

if __name__ == '__main__':
    unittest.main()
