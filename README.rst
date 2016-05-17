========
aioredux
========

|pypi| |travis| |downloads|

Pythonic `Redux <https://github.com/rackt/redux>`_

Pythonic `Redux <https://github.com/rackt/redux>`_ using asyncio. ``aioredux``
provides a predictable state container with the following goal: "[Redux] helps
you write applications that behave consistently, run in different environments
..., and are easy to test" (from the `Redux <https://github.com/rackt/redux>`_
documentation).

* Free software: Mozilla Public License

**This package requires Python 3.4 or higher**

Usage
-----
::

   import asyncio
   import aioredux

    async def go():
        initial_state = {
            'todos': (),
        }

        def add_todo(text):
            return {'type': 'ADD_TODO', 'text': text}

        def reducer(state, action):
            if action['type'] == 'ADD_TODO':
                todos = state['todos'] + (action['text'],)
                return {'todos': todos}
            return state

        store = yield from aioredux.create_store(reducer, initial_state)
        yield from store.dispatch(add_todo('todo text'))
        print(store.state['todos'])

    asyncio.get_event_loop().run_until_complete(go())


Implementation notes
--------------------
-  ``dispatch`` is marked as ``async`` although in most cases it functions like
   a plain Python function returning a Future. This is done to allow for cases
   where dispatch performs a more complicated set of (async) actions.
-  A Pythonic version of `redux-thunk <https://github.com/gaearon/redux-thunk>`_ is also included.


.. |pypi| image:: https://badge.fury.io/py/aioredux.png
    :target: https://badge.fury.io/py/aioredux
    :alt: pypi version

.. |travis| image:: https://travis-ci.org/ariddell/aioredux.png?branch=master
    :target: https://travis-ci.org/ariddell/aioredux
    :alt: travis-ci build status

.. |downloads| image:: https://img.shields.io/pypi/dm/aioredux.svg
    :target: https://pypi.python.org/pypi/aioredux
    :alt: pypi download statistics
