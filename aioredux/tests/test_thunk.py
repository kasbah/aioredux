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


class TestThunk(base.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        super().setUp()

    def tearDown(self):
        self.loop.close()
        self.loop = None
        super().tearDown()

    def test_todo_thunk(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }

            def add_todo(text):
                return {'type': 'ADD_TODO', 'text': text}

            def reducer(state, action):
                if action['type'] == 'ADD_TODO':
                    todos = state['todos'] + (action['text'],)
                    return toolz.assoc(state, 'todos', todos)
                return state

            create_store_partial = functools.partial(aioredux.create_store, loop=self.loop)
            create_store_with_middleware = aioredux.apply_middleware(aioredux.middleware.thunk_middleware)(create_store_partial)  # noqa
            store = yield from create_store_with_middleware(reducer, initial_state)
            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 0)

            @coroutine
            def thunk(dispatch, state_func):
                yield from dispatch(add_todo('todo text'))

            yield from store.dispatch(thunk)
            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 1)

        self.loop.run_until_complete(go())

    def test_todo_thunk_return_value(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }

            def add_todo(text):
                return {'type': 'ADD_TODO', 'text': text}

            def add_todo_complex():
                @coroutine
                def thunk(dispatch, state_func):
                    yield from dispatch({'type': 'ADD_TODO', 'text': 'todo text'})
                    return 19
                return thunk

            def reducer(state, action):
                if action['type'] == 'ADD_TODO':
                    todos = state['todos'] + (action['text'],)
                    return toolz.assoc(state, 'todos', todos)
                return state

            create_store_partial = functools.partial(aioredux.create_store, loop=self.loop)
            create_store_with_middleware = aioredux.apply_middleware(aioredux.middleware.thunk_middleware)(create_store_partial)  # noqa
            store = yield from create_store_with_middleware(reducer, initial_state)

            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 0)
            # use a thunk
            return_value = yield from store.dispatch(add_todo_complex())
            self.assertEqual(return_value, 19)
            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 1)

        self.loop.run_until_complete(go())

    def test_todo_thunk_async(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }

            def add_todo(text):
                return {'type': 'ADD_TODO', 'text': text}

            def add_todo_slow():
                @coroutine
                def thunk(dispatch, state_func):
                    yield from asyncio.sleep(0.01, loop=self.loop)
                    yield from dispatch(add_todo('slow todo'))
                return thunk

            def reducer(state, action):
                if action['type'] == 'ADD_TODO':
                    todos = state['todos'] + (action['text'],)
                    return toolz.assoc(state, 'todos', todos)
                return state

            create_store_partial = functools.partial(aioredux.create_store, loop=self.loop)
            create_store_with_middleware = aioredux.apply_middleware(aioredux.middleware.thunk_middleware)(create_store_partial)  # noqa
            store = yield from create_store_with_middleware(reducer, initial_state)

            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 0)
            yield from store.dispatch(add_todo('first todo'))
            self.assertIsNotNone(store.state)
            self.assertEqual(len(store.state['todos']), 1)

            yield from store.dispatch(add_todo_slow())
            yield from asyncio.sleep(0.02, loop=self.loop)
            self.assertIsNotNone(store.state)
            self.assertEqual(len(store.state['todos']), 2)

        self.loop.run_until_complete(go())
