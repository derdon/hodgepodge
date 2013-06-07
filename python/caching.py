from collections import OrderedDict, Counter


class Cache(OrderedDict):
    def __init__(self, maxsize=float('inf')):
        self.maxsize = maxsize
        OrderedDict.__init__(self)

    @property
    def is_full(self):
        return len(self) >= self.maxsize


class LRUCache(Cache):
    def __setitem__(self, key, value):
        if self.is_full:
            self.popitem(last=False)
        Cache.__setitem__(self, key, value)


class LFUCache(Cache):
    def __init__(self, maxsize=float('inf')):
        self.usage_counter = Counter()
        Cache.__init__(self, maxsize)

    def _get_lfu_key(self):
        min_ = float('inf')
        for k, v in self.usage_counter.iteritems():
            if v < min_:
                min_ = v
                key = k
        return key

    def __getitem__(self, key):
        value = Cache.__getitem__(self, key)
        self.usage_counter[key] += 1
        return value

    def __setitem__(self, key, value):
        self.usage_counter[key] += 1
        if self.is_full:
            lfu_key = self._get_lfu_key()
            del self[lfu_key]
            del self.usage_counter[lfu_key]
        Cache.__setitem__(self, key, value)


def test_lru_cache():
    lrucache = LRUCache(3)
    lrucache[1] = 'a'
    lrucache[2] = 'b'
    lrucache[3] = 'c'
    lrucache[1] = 'a'
    lrucache[4] = 'd'
    assert len(lrucache) == 3
    assert lrucache.items() == [(3, 'c'), (1, 'a'), (4, 'd')]


def test_lfu_cache():
    lfucache = LFUCache(3)
    lfucache[1] = 'a'
    lfucache[2] = 'b'
    lfucache[3] = 'c'
    lfucache[1]
    lfucache[2]
    lfucache[4] = 'd'
    assert len(lfucache) == 3
    assert lfucache.items() == [(1, 'a'), (2, 'b'), (4, 'd')]


if __name__ == '__main__':
    test_lru_cache()
    test_lfu_cache()
