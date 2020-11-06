#!/usr/bin/env python

import datetime
import logging
import subprocess
import time
import unittest

import memcache
from memcacheinspector import *

logging.basicConfig(level=logging.DEBUG)


# These tests assume that memcached is already running.

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
    mc = MC

    def setUp(self):
        for i in range(len(self.mc)):
            self.mc[i]['client'].set('foo', 'bar')
            self.mc[i]['client'].set('myaddr', self.mc[i]['addr'])
            if i == 0:
                self.mc[i]['client'].set('just_for_first', 'special')
            elif i == (len(self.mc) - 1):
                self.mc[i]['client'].set('just_for_last', 'also special')

    def tearDown(self):
        for mc in self.mc:
            mc['client'].flush_all()


    def assertContains(self, itemset, expected_item, hosts=None, ignore_expiration=False):
        if not hosts:
            hosts = [mc['addr'] for mc in self.mc]
        for host in hosts:
            if not host in itemset:
                self.fail('%s does not have any items.' % (host,))
            ok = False
            for item in itemset[host]:
                if item.equals(expected_item, ignore_expiration=ignore_expiration):
                    ok = True
            if not ok:
                self.fail('%s does not have an equivalent item with key %s' % (host, expected_item.key))

    single_client_tests = (
        mc[0]['addr'],
        mc[0]['client'],
        (mc[0]['addr'],),
        (mc[0]['client'],),
    )
    def _singleClientItems(self, itemset, give_values=True):
        item = MemcacheItem('foo', 3, self.now, value='bar' if give_values else None)
        self.assertContains(itemset, item, hosts=[self.mc[0]['addr']], ignore_expiration=True)

        item = MemcacheItem('myaddr', len(self.mc[0]['addr']), self.now, value=self.mc[0]['addr'] if give_values else None)
        self.assertContains(itemset, item, hosts=[self.mc[0]['addr']], ignore_expiration=True)

    def testSingleClient(self):
        for test in self.single_client_tests:
            mci = MemcacheInspector(test)
            self._singleClientItems(mci.get_items(include_values=True))

    def testGetItemsSingleClient(self):
        for test in self.single_client_tests:
            self._singleClientItems(get_items(test, include_values=True))

    def testSingleClientNoValues(self):
        for test in self.single_client_tests:
            mci = MemcacheInspector(test)
            self._singleClientItems(mci.get_items(include_values=False), give_values=False)

    def testGetItemsSingleClientNoValues(self):
        for test in self.single_client_tests:
            self._singleClientItems(get_items(test, include_values=False), give_values=False)


    multiple_client_tests = (
        (mc[0]['addr'], mc[1]['addr']),
        (mc[0]['addr'], mc[1]['client']),
        (mc[0]['client'], mc[1]['addr']),
        (mc[0]['client'], mc[1]['client']),
    )
    def _multipleClientItems(self, itemset, give_values=True):
        item = MemcacheItem('foo', 3, self.now, value='bar' if give_values else None)
        self.assertContains(itemset, item, ignore_expiration=True)

        for i in range(len(self.mc)):
            item = MemcacheItem('myaddr', len(self.mc[i]['addr']), self.now, value=self.mc[i]['addr'] if give_values else None)
            self.assertContains(itemset, item, hosts=[self.mc[i]['addr']], ignore_expiration=True)

        item = MemcacheItem('just_for_first', 7, self.now, value='special' if give_values else None)
        self.assertContains(itemset, item, hosts=[self.mc[0]['addr']], ignore_expiration=True)
        item = MemcacheItem('just_for_last', 12, self.now, value='also special' if give_values else None)
        self.assertContains(itemset, item, hosts=[self.mc[len(self.mc) - 1]['addr']], ignore_expiration=True)

    def testMultipleClients(self):
        for test in self.multiple_client_tests:
            mci = MemcacheInspector(test)
            self._multipleClientItems(mci.get_items(include_values=True))

    def testGetItemsMultipleClients(self):
        for test in self.multiple_client_tests:
            self._multipleClientItems(get_items(test, include_values=True))

    def testMultipleClientsNoValues(self):
        for test in self.multiple_client_tests:
            mci = MemcacheInspector(test)
            self._multipleClientItems(mci.get_items(include_values=False), give_values=False)

    def testGetItemsMultipleClientsNoValues(self):
        for test in self.multiple_client_tests:
            self._multipleClientItems(get_items(test, include_values=False), give_values=False)


if __name__ == '__main__':
    unittest.main()
