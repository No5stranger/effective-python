# -*- coding: utf-8 -*-

import time
from threading import Thread, Lock


class Counter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset=1):
        self.count += offset

    def increment_with_lock(self, offset=1):
        with self.lock:
            self.count += offset


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # counter.increment()
        counter.increment_with_lock()


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

start = time.time()
how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
end = time.time()
time_cost = end - start
print('Counter should be %d, found %d' % (5 * how_many, counter.count))
print('Time cost: %.8f' % time_cost)


'''
Without lock:
    Counter should be 500000, found 263148
    Time cost: 0.22897410

With lock:
    Counter should be 500000, found 500000
    Time cost: 2.76215005
'''
