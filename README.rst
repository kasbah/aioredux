========
aioredux
========

Pythonic `Redux <https://github.com/rackt/redux>`_

Pythonic `Redux <https://github.com/rackt/redux>`_ using asyncio. ``aioredux``
provides a predictable state container with the following goal: "[Redux] helps
you write applications that behave consistently, run in different environments
..., and are easy to test" (from the `Redux <https://github.com/rackt/redux>`_
documentation).

* Free software: Mozilla Public License

**This package requires Python 3.4 or higher**

Implementation notes
--------------------
- `dispatch` is a marked as `async` although in most cases it functions like
  a plain Python function returning a Future. This is done to allow for cases
  where dispatch performs a more complicated set of (async) actions.
