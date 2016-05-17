import asyncio
import functools

import toolz

import aioredux
import aioredux.middleware
from aioredux.tests import base
import aioredux.utils

try:
    from types import coroutine
except ImportError:
    from asyncio import coroutine


class TestThunkNested(base.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        super().setUp()

    def tearDown(self):
        self.loop.close()
        self.loop = None
        super().tearDown()

    def test_todo_thunk_nested(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }

            def add_todo(text):
                return {'type': 'ADD_TODO', 'text': text}

            def add_todo_thunk_nested():
                @coroutine
                def thunk(dispatch, state_func):
                    yield from dispatch({'type': 'ADD_TODO', 'text': 'todo text'})
                    return 5
                return thunk

            def add_todo_thunk():
                @coroutine
                def thunk(dispatch, state_func):
                    yield from dispatch(add_todo_thunk_nested())
                    return 3
                return thunk

            def reducer(state, action):
                if action['type'] == 'ADD_TODO':
                    todos = state['todos'] + (action['text'],)
                    return toolz.assoc(state, 'todos', todos)
                return state

            create_store_partial = functools.partial(aioredux.create_store, loop=self.loop)
            create_store_with_middleware = aioredux.apply_middleware(aioredux.middleware.thunk_middleware)(create_store_partial)  # noqa
            store = yield from create_store_with_middleware(reducer, initial_state)

            self.assertEqual(len(store.state['todos']), 0)
            # first make sure the nested thunk works as expected
            return_value = yield from store.dispatch(add_todo_thunk_nested())
            self.assertEqual(return_value, 5)
            self.assertEqual(len(store.state['todos']), 1)
            # now test the thunk dispatching a thunk
            return_value = yield from store.dispatch(add_todo_thunk())
            self.assertEqual(return_value, 3)
            self.assertEqual(len(store.state['todos']), 2)

        self.loop.run_until_complete(go())
