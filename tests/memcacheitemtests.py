#!/usr/bin/env python

import datetime
import time
import unittest

from memcacheinspector import *


class MemcacheItemTests(unittest.TestCase):
    now_time = time.time()
    now = datetime.datetime.fromtimestamp(now_time)

    good_constructor_tests = (
        (('foo', 'foo'), (5, 5), (now, now)),

        ((123, '123'), (5, 5), (now, now)),

        (('foo', 'foo'), ('5', 5), (now, now)),
        (('foo', 'foo'), (5.67, 5), (now, now)),
        (('foo', 'foo'), ('5.67', 5), (now, now)),

        (('foo', 'foo'), (5, 5), (123, datetime.datetime.fromtimestamp(123))),
        (('foo', 'foo'), (5, 5), ('123', datetime.datetime.fromtimestamp(123))),
        (('foo', 'foo'), (5, 5), (1234.56, datetime.datetime.fromtimestamp(1234.56))),
        (('foo', 'foo'), (5, 5), ('1234.56', datetime.datetime.fromtimestamp(1234.56))),
        (('foo', 'foo'), (5, 5), (now_time, now)),
    )
    def testConstructorGood(self):
        for test in self.good_constructor_tests:
            mki = MemcacheItem(test[0][0], test[1][0], test[2][0])
            self.assertEqual(test[0][1], mki.key)
            self.assertEqual(test[1][1], mki.size)
            self.assertEqual(test[2][1], mki.expiration)


    bad_constructor_tests = (
        (None, 5, now),

        ('foo', None, now),
        ('foo', 'bar', now),
        ('foo', -1, now),
        ('foo', '-1', now),
        ('foo', [5], now),

        ('foo', 5, None),
        ('foo', 5, 'bar'),
        ('foo', 5, [123]),
    )
    def testConstructorBad(self):
        for test in self.bad_constructor_tests:
            self.assertRaises(MemcacheInspectorError, MemcacheItem, test[0], test[1], test[2])


    equality_tests = (
        (MemcacheItem('foo', 3, now), MemcacheItem('foo', 3, now)),
        (MemcacheItem('foo', 3, now, value='bar'), MemcacheItem('foo', 3, now, value='bar')),
    )
    def testEquality(self):
        for test in self.equality_tests:
            self.assertEqual(test[0], test[1])

    nonexp_equality_tests = (
        (MemcacheItem('foo', 3, now), MemcacheItem('foo', 3, datetime.datetime.fromtimestamp(123))),
        (MemcacheItem('foo', 3, now, value='bar'), MemcacheItem('foo', 3, datetime.datetime.fromtimestamp(123), value='bar')),
    )
    def testNonExpEquality(self):
        for test in self.nonexp_equality_tests:
            self.assertTrue(test[0].equals(test[1], ignore_expiration=True))


    inequality_tests = (
        (MemcacheItem('foo', 3, now), MemcacheItem('f00', 3, now)),
        (MemcacheItem('foo', 3, now), MemcacheItem('foo', 5, now)),
        (MemcacheItem('foo', 3, now), MemcacheItem('foo', 3, datetime.datetime.fromtimestamp(123))),
        (MemcacheItem('foo', 3, now, value='bar'), MemcacheItem('foo', 3, now, value='baz')),
    )
    def testInequality(self):
        for test in self.inequality_tests:
            self.assertNotEqual(test[0], test[1])

    nonexp_inequality_tests = (
        (MemcacheItem('foo', 3, now), MemcacheItem('f00', 3, datetime.datetime.fromtimestamp(123))),
        (MemcacheItem('foo', 3, now), MemcacheItem('foo', 5, datetime.datetime.fromtimestamp(123))),
        (MemcacheItem('foo', 3, now, value='bar'), MemcacheItem('foo', 3, datetime.datetime.fromtimestamp(123), value='baz')),
    )
    def testNonExpInequality(self):
        for test in self.nonexp_inequality_tests:
            self.assertFalse(test[0].equals(test[1], ignore_expiration=True))


if __name__ == '__main__':
    unittest.main()
