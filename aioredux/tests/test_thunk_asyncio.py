import asyncio
import functools

import toolz

import aioredux
import aioredux.middleware
import aioredux.utils
from aioredux.tests import base


class TestThunkAsync(base.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        super().setUp()

    def test_todo_thunk_async(self):
        @asyncio.coroutine
        def run():
            initial_state = {
                'todos': (),
            }

            def add_todo(text):
                return {'type': 'ADD_TODO', 'text': text}

            def add_todo_slow():
                @asyncio.coroutine
                def thunk(dispatch, state_func):
                    dispatch(add_todo('slow todo'))
                return thunk

            def reducer(state, action):
                if action['type'] == 'ADD_TODO':
                    todos = state['todos'] + (action['text'],)
                    return toolz.assoc(state, 'todos', todos)
                return state

            thunk_middleware = functools.partial(aioredux.middleware.thunk_middleware, loop=self.loop)
            create_store_with_middleware = aioredux.apply_middleware(thunk_middleware)(aioredux.Store)
            store = create_store_with_middleware(reducer, initial_state)

            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 0)
            store.dispatch(add_todo('first todo'))
            self.assertIsNotNone(store.state)
            self.assertEqual(len(store.state['todos']), 1)

            store.dispatch(add_todo_slow())
            yield from asyncio.sleep(0.1, loop=self.loop)
            print(store.state)
            self.assertIsNotNone(store.state)
            self.assertEqual(len(store.state['todos']), 2)

        self.loop.run_until_complete(run())
