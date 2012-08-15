#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for pydstat object setup.

Source:: https://github.com/ampledata/pydstat
"""


import random
import unittest

from context import pydstat


class TestPydStat(unittest.TestCase):
    """Tests for pydstat."""

    def setUp(self):
        self.rands = ''.join(
            [random.choice('unittest0123456789') for xyz in range(8)])

    def test_default_log_dest(self):
        pyds = pydstat.PydStat()
        pyds.get_stats()

    def test_alt_log_dest(self):
        pyds = pydstat.PydStat(log_dest=('localhost', 514))
        pyds.get_stats()

    def test_no_pidstat(self):
        self.assertRaises(
            pydstat.PydStatError, pydstat.PydStat, pidstat=self.rands)

if __name__ == '__main__':
    unittest.main()
