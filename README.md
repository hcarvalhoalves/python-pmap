# python-pmap

[Clojure's pmap](https://clojuredocs.org/clojure.core/pmap) implementation for Python.

Multi-threaded versions of the following high-order functions are available:

| fn              | equivalent to
| -------------   | ---------------------
| `pmap.pmap`     | `itertools.imap`
| `pmap.pvalmap`  | `toolz.dictoolz.valmap`
| `pmap.pkeymap`  | `toolz.dictoolz.keymap`

Package also includes `pmap.Deferred` and `pmap.Future` classes that may be generally useful.

See included `tests/` for usage examples.