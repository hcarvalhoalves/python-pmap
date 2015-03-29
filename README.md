[Clojure's pmap](https://clojuredocs.org/clojure.core/pmap) implementation for Python.

### Usage

```
from pmap import pmap

def fn(ele):
	return do_some_IO(ele)

seq = xrange(10000)

for result in pmap(fn, seq):
	print result

```