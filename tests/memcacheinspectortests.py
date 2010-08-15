#!/usr/bin/env python

import datetime
import logging
import subprocess
import time
import unittest

import memcache
from memcacheinspector import *

logging.basicConfig(level=logging.DEBUG)


# These tests assume that memcache is already running.

_PORT = 11222
MC = []
for i in range(2):
    mc = {}
    mc['addr'] = '127.0.0.1:%s' % (_PORT,)
    mc['client'] = memcache.Client([mc['addr']])
    _PORT += 1
    MC.append(mc)


class MemcacheInspectorTests(unittest.TestCase):
    now_time = time.time()
    now = datetime.datetime.fromtimestamp(now_time)

    def setUp(self):
        global MC
        for i in range(len(MC)):
            MC[i]['client'].set('foo', 'bar')
            MC[i]['client'].set('myaddr', MC[i]['addr'])
            if i == 0:
                MC[i]['client'].set('just_for_first', 'special')
            elif i == (len(MC) - 1):
                MC[i]['client'].set('just_for_last', 'also special')

    def tearDown(self):
        global MC
        for mc in MC:
            mc['client'].flush_all()


    def assertContains(self, itemset, expected_item, hosts=None, ignore_expiration=False):
        global MC
        if not hosts:
            hosts = [mc['addr'] for mc in MC]
        for host in hosts:
            if not itemset.has_key(host):
                self.fail('%s does not have any items.' % (host,))
            ok = False
            for item in itemset[host]:
                if item.equals(expected_item, ignore_expiration=ignore_expiration):
                    ok = True
            if not ok:
                self.fail('%s does not have an equivalent item with key %s' % (host, expected_item.key))


    def testSingleClient(self):
        global MC
        tests = (
            MC[0]['addr'],
            MC[0]['client'],
            (MC[0]['addr'],),
            (MC[0]['client'],),
        )
        for test in tests:
            mci = MemcacheInspector(test)

            item = MemcacheItem('foo', 3, self.now, value='bar')
            self.assertContains(mci.get_items(include_values=True), item, hosts=[MC[0]['addr']], ignore_expiration=True)

            item = MemcacheItem('myaddr', len(MC[0]['addr']), self.now, value=MC[0]['addr'])
            self.assertContains(mci.get_items(include_values=True), item, hosts=[MC[0]['addr']], ignore_expiration=True)


    def testMultipleClients(self):
        global MC
        tests = (
            (MC[0]['addr'], MC[1]['addr']),
            (MC[0]['addr'], MC[1]['client']),
            (MC[0]['client'], MC[1]['addr']),
            (MC[0]['client'], MC[1]['client']),
        )
        for test in tests:
            mci = MemcacheInspector(test)

            item = MemcacheItem('foo', 3, self.now, value='bar')
            self.assertContains(mci.get_items(include_values=True), item, ignore_expiration=True)

            for i in range(len(MC)):
                item = MemcacheItem('myaddr', len(MC[i]['addr']), self.now, value=MC[i]['addr'])
                self.assertContains(mci.get_items(include_values=True), item, hosts=[MC[i]['addr']], ignore_expiration=True)

            item = MemcacheItem('just_for_first', 7, self.now, value='special')
            self.assertContains(mci.get_items(include_values=True), item, hosts=[MC[0]['addr']], ignore_expiration=True)
            item = MemcacheItem('just_for_last', 12, self.now, value='also special')
            self.assertContains(mci.get_items(include_values=True), item, hosts=[MC[len(MC) - 1]['addr']], ignore_expiration=True)


if __name__ == '__main__':
    unittest.main()
