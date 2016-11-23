import time
import traceback

from pmap.core import *


def always_fail(x):
    raise ValueError(x)


def maybe_fail(x):
    return always_fail(x)


def timeit(f):
    t = time.time()
    f()
    return time.time() - t


def test_future_deref():
    f = Future(lambda x: 21 * x)
    assert f(2).deref(1) == 42


def test_future_deref_raise_original_traceback():
    f = Future(maybe_fail)
    try:
        f("Monday").deref(1)
    except ValueError as e:
        assert str(e) == "Monday"
        frames = traceback.extract_tb(sys.exc_info()[2])
        # Traceback points to the original function throwing the exception
        assert frames[-1][2] == 'always_fail'
        # Traceback contains the line throwing the exception
        assert frames[-1][3] == 'raise ValueError(x)'
        # Traceback contains parent
        assert frames[-2][2] == 'maybe_fail'
        assert frames[-2][3] == 'return always_fail(x)'


def test_future_timeout():
    def slow_future():
        time.sleep(10)

    f = Future(slow_future)
    try:
        f.deref(1)
    except multiprocessing.TimeoutError as e:
        pass


def test_pmap():
    def square(x):
        return x ** 2

    # Fast fns have negligible overhead
    t0 = time.time()
    result = list(pmap(square, xrange(100)))
    t1 = time.time()
    assert t1 - t0 < 0.1
    # Results keep ordering
    assert result == list(map(square, xrange(100)))

    def slow_square(x):
        time.sleep(0.01)
        return x ** 2

    # Slow fns scale sub-linear w/ respect to number of threads
    t0 = time.time()
    result = list(pmap(slow_square, xrange(100), threads=100))
    t1 = time.time()
    assert t1 - t0 < 10.0
    # Results keep ordering
    assert result == list(map(square, xrange(100)))


def test_pmap_raise_original_traceback():
    try:
        list(pmap(always_fail, ['foo']))
    except ValueError:
        frames = traceback.extract_tb(sys.exc_info()[2])
        print frames
        assert frames[-1][2] == 'always_fail'
        assert frames[-1][3] == 'raise ValueError(x)'
