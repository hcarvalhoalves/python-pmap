# Changelog

## [1.1.0]
### New
- `Future` now takes a `pool` argument to specify a thread pool.
- `Future` now implements `__call__` to allow `Future(f)("foo", k=42)` style to pass additional arguments.
- `Future.deref()` now accepts an optional `timeout` parameter to avoid blocking forever.
- Introduce `Deferred` object to encapsulate deferred results and re-throwing with original traceback.

## [1.0.3]
### New
- Keep original traceback when re-throwing errors on realization of `pmap` generator.

## [1.0.0]
### New
- Introduce `pmap` function for mapping over collection (lazily) in parallel.