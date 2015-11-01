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

Usage
-----

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
    print(store.state['todos')


Implementation notes
--------------------
- `dispatch` is a marked as `async` although in most cases it functions like
  a plain Python function returning a Future. This is done to allow for cases
  where dispatch performs a more complicated set of (async) actions.
