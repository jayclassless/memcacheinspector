import datetime
import memcache


__version__ = (0, 1, 0)


class MemcacheKeyInfo:
    def __init__(self, name, size, expiration):
        self.name = name
        self.size = size
        self.expiration = expiration

    def __str__(self):
        return '%s (%sb)' % (self.key, self.size)


class MemcacheInspector:
    def __init__(self, hosts):
        if isinstance(hosts, list) or isinstance(hosts, tuple):
            self.clients = self._build_clients(hosts)
        else:
            self.clients = self._build_clients([hosts])

    def _build_clients(self, hosts):
        clients = []
        for host in hosts:
            if isinstance(host, memcache.Client):
                clients.append(host)
            else:
                clients.append(memcache.Client([host]))
        return clients

    def _get_server(self, mc):
        server = mc.servers[0]
        server.connect()
        return server

    def _get_hostname(self, mc):
        server = self._get_server(mc)
        return '%s:%s' % (server.ip, server.port)

    def _get_slabs(self, mc):
        server = self._get_server(mc)
        server.send_cmd('stats slabs')
        slabs = []
        while True:
            stats = server.readline()
            if stats == 'END':
                break
            tokens = stats.split()
            slabinfo = tokens[1].split(':')
            if len(slabinfo) > 1 and slabinfo[1] == 'chunk_size':
                slabs.append(slabinfo[0])
        return slabs

    def _get_keys(self, mc):
        server = self._get_server(mc)
        keys = []
        for slab in self._get_slabs(mc):
            server.send_cmd('stats cachedump %s 0' % (slab,))
            while True:
                item = server.readline()
                if item == 'END':
                    break
                tokens = item.split(None, 2)
                size = expiration = 0
                for attr in tokens[2].strip('[]').split(';'):
                    val, type = attr.split()
                    try:
                        if type == 'b':
                            size = int(val)
                        elif type == 's':
                            expiration = int(val)
                    except ValueError:
                        pass
                keys.append(MemcacheKeyInfo(tokens[1], size, datetime.datetime.fromtimestamp(expiration)))
        return keys

    def get_key_info(self):
        keys = {}
        for client in self.clients:
            keys[self._get_hostname(client)] = self._get_keys(client)
        return keys

    def dump_all(self, max_size=0):
        keypairs = {}
        for client in self.clients:
            keys = [ki.name for ki in self._get_keys(client) if max_size <= 0 or ki.size <= max_size]
            keypairs[self._get_hostname(client)] = client.get_multi(keys)
        return keypairs

