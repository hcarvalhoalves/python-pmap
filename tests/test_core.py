import time
import traceback

from pmap.core import *


def timeit(f):
    t = time.time()
    f()
    return time.time() - t


def test_future_deref():
    f = Future(lambda: True)
    assert f.deref() == True


def test_future_timing():
    def slow_future():
        time.sleep(0.3)

    t0 = time.time()
    f = Future(slow_future)
    assert time.time() - t0 < 0.1
    f.deref()
    assert time.time() - t0 > 0.3


def test_pmap():
    def square(x):
        return x ** 2

    def slow_square(x):
        time.sleep(0.04)
        return x ** 2

    t0 = time.time()
    result = pmap(square, xrange(100))
    assert time.time() - t0 < 0.01
    assert list(result) == list(map(square, xrange(100)))

    t0 = time.time()
    result = pmap(slow_square, xrange(100))
    assert time.time() - t0 < 0.2
    assert list(result) == list(map(square, xrange(100)))


def test_exception_handling():
    def deep_func(x):
        raise ValueError(x)

    def fail_func(x):
        return deep_func(x)

    try:
        list(pmap(fail_func, ['foo']))
    except:
        frames = traceback.extract_tb(sys.exc_info()[2])
        last_frame = frames[-1]
        # Stacktrace points to the original function throwing the exception
        assert last_frame[2] == 'deep_func'
        # Stacktrace contains the line throwing the exception
        assert last_frame[3] == 'raise ValueError(x)'
