import sys
import time
import contextlib
import itertools
import multiprocessing
import threading
import Queue

_num_cores = multiprocessing.cpu_count


@contextlib.contextmanager
def threaded(*args, **kwargs):
    t = threading.Thread(*args, **kwargs)
    t.daemon = True     # Allow terminating by killing the parent with ^C
    t.start()
    try:
        yield
    finally:
        t.join()


def seque(seq):
    """
    Consume seq in a separate thread, passing it to the calling
    thread in a queue.
    """
    DONE = "_________XXXX___________DONE_ZZ"
    q = Queue.Queue()

    def wrapper():
        for el in seq:
            q.put(el)
        q.put(DONE)

    with threaded(target=wrapper):
        while True:
            el = q.get()
            if el == DONE:
                break
            yield el


class Future(object):
    """
    Futures implementation.

    https://en.wikipedia.org/wiki/Futures_and_promises
    """
    def __init__(self, func):
        self.e = None
        self.done = threading.Event()
        def wrapper():
            try:
                self.value = func()
            except Exception as e:
                self.e = e
            finally:
                self.done.set()
        self.thread = threading.Thread(target=wrapper)
        self.thread.daemon = True
        self.thread.start()

    def deref(self):
        self.done.wait()
        if self.e:
            raise self.e.__class__, self.e, sys.exc_info()[2]
        return self.value


def partition_all(n, seq):
    """
    Partition `seq` in blocks of `n` elements.
    """
    it = iter(seq)
    while True:
        block = list(itertools.islice(it, n))
        if not block:
            break
        yield block


def pmap(f, seq, threads=None):
    """
    Apply `f` to each element of `seq` in at most N `threads`.
    
    Returns a generator and yields as soon as results are available.

    By default will spawn one thread per available core, but
    for I/O bound tasks it's useful to define `threads = len(seq)`,
    as long as `threads` < maximum number of threads per proc.
    """
    threads = threads or _num_cores()
    assert type(threads) == int
    partitioned = partition_all(threads, seq)
    for subseq in partitioned:
        threads = list(map(lambda z: Future(lambda: f(z)), subseq))
        for th in threads:
            yield th.deref()
