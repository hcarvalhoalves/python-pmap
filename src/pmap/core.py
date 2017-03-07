import multiprocessing
import multiprocessing.pool
import sys
import threading


class Deferred(object):
    """
    Construct the equivalent of a delayed `func`, delaying exceptions until `.deref()`.
    If `func` failed, re-throws with original traceback on `.deref()`.

    Example:
        >>> Deferred(lambda x: x * 2)(2).deref()
        4
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            self.value, self.exc_info = self.func(*args, **kwargs), None
        except Exception as e:
            self.value, self.exc_info = None, sys.exc_info()
        return self

    def deref(self):
        # Allows calling without arguments if not called explicitly before deref
        if not hasattr(self, 'value'):
            self.__call__()
        if self.exc_info:
            raise self.exc_info[0], self.exc_info[1], self.exc_info[2]
        return self.value


class Future(object):
    """
    Futures implementation.
    https://en.wikipedia.org/wiki/Futures_and_promises

    Will spawn a Thread for each instance, unless a pool is specified.

    This object is mostly useful for I/O-bound tasks, or if the passed func knows how to release the GIL
    (https://wiki.python.org/moin/GlobalInterpreterLock) efficiently for CPU-bound tasks.

    Example:
        >>> import time
        >>> Future(lambda x: time.sleep(x) and x)(1).deref(timeout=2)
        1

    """

    def __init__(self, func, pool=None):
        self.func = func
        self.done = None
        self.pool = pool or multiprocessing.pool.ThreadPool()

    def __call__(self, *args, **kwargs):
        self.done = threading.Event()
        self.pool.apply_async(Deferred(self.func),
                              args=args, kwds=kwargs, callback=self._set_result_and_done)
        return self

    def _set_result_and_done(self, deferred):
        self.deferred = deferred
        self.done.set()

    def deref(self, timeout=None):
        # Allows calling without arguments if not called explicitly before deref
        if not self.done:
            self.__call__()
        if not self.done.wait(timeout):
            raise multiprocessing.TimeoutError("{} timed out after {} second.".format(
                self.func, timeout))
        return self.deferred.deref()


def pmap(f, seq, threads=None, timeout=None):
    """
    Apply `f` to each element of `seq` in at most N `threads`.

    `f` is expected to be a one-arity function.

    Returns a generator and yields as soon as results become available. Keeps ordering of original sequence.

    By default will spawn one thread per available core, but for I/O bound tasks it might be useful to define
    `threads` higher, to saturate throughput.
    """
    assert (threads is None) or (type(threads) is int)
    assert (timeout is None) or (type(timeout) is int)
    pool = multiprocessing.pool.ThreadPool(threads)
    assert hasattr(pool, 'apply_async')
    # Instantiate all futures so work can start in background thread pool
    fpool = [Future(f, pool=pool)(ele) for ele in seq]
    # Return a lazy generator that will block for results as necessary
    return (f.deref(timeout) for f in fpool)
