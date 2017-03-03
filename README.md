[Clojure's pmap](https://clojuredocs.org/clojure.core/pmap) implementation for Python.

### Usage of pmap

```
from pmap import pmap

def fn(ele):
	return do_some_IO(ele)

seq = xrange(10000)

for result in pmap(fn, seq):
	print result

```


### Usage of pvalmap

```
from pmap import pvalmap

def fn(ele):
	return do_some_IO(ele)

d = some_dict

dict(pvalmap(d))

```
