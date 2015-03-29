import time
import unittest
from .core import *


def timeit(f):
    t = time.time()
    f()
    return time.time() - t


class PMapTest(unittest.TestCase):
    def test_future_deref(self):
        f = Future(lambda: True)
        self.assertTrue(f.deref() == True)

    def test_future_timing(self):
        def slow_future():
            time.sleep(0.3)

        t0 = time.time()
        f = Future(slow_future)
        self.assertTrue(time.time() - t0 < 0.1)
        f.deref()
        self.assertTrue(time.time() - t0 > 0.3)

    def test_pmap(self):
        def square(x):
            return x ** 2

        def slow_square(x):
            time.sleep(0.04)
            return x ** 2

        t0 = time.time()
        result = pmap(square, xrange(100))
        self.assertTrue(time.time() - t0 < 0.01)
        self.assertTrue(list(result) == list(map(square, xrange(100))))

        t0 = time.time()
        result = pmap(slow_square, xrange(100))
        self.assertTrue(time.time() - t0 < 0.2)
        self.assertTrue(list(result) == list(map(square, xrange(100))))

if __name__ == "__main__":
    unittest.main()
