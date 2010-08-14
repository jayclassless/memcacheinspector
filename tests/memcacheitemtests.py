#!/usr/bin/env python

import datetime
import time
import unittest

import memcacheinspector


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


    def testConstructorGood(self):
        for test in self.good_constructor_tests:
            mki = memcacheinspector.MemcacheItem(test[0][0], test[1][0], test[2][0])
            self.assertEqual(test[0][1], mki.key)
            self.assertEqual(test[1][1], mki.size)
            self.assertEqual(test[2][1], mki.expiration)

    def testConstructorBad(self):
        for test in self.bad_constructor_tests:
            self.assertRaises(memcacheinspector.MemcacheInspectorError, memcacheinspector.MemcacheItem, test[0], test[1], test[2])


if __name__ == '__main__':
    unittest.main()
