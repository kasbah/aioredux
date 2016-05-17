import asyncio

import toolz

import aioredux
from aioredux.tests import base

try:
    from types import coroutine
except ImportError:
    from asyncio import coroutine


class TestBasic(base.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        super().setUp()

    def tearDown(self):
        self.loop.close()
        self.loop = None
        super().tearDown()

    def test_todo(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }
            store = yield from aioredux.create_store(lambda state, action: state, initial_state, loop=self.loop)
            self.assertIsNotNone(store)
            self.assertIsNotNone(store.state)

        self.loop.run_until_complete(go())

    def test_todo_reducer(self):

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

            store = yield from aioredux.create_store(reducer, initial_state, loop=self.loop)
            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 0)
            yield from store.dispatch(add_todo('todo text'))
            self.assertIsNotNone(store.state)
            self.assertIsNotNone(store.state['todos'])
            self.assertEqual(len(store.state['todos']), 1)

        self.loop.run_until_complete(go())

    def test_subscribe(self):

        @coroutine
        def go():
            initial_state = {
                'todos': (),
            }
            store = yield from aioredux.create_store(lambda state, action: state, initial_state, loop=self.loop)
            self.assertEqual(len(store.listeners), 0)
            unsubscribe = store.subscribe(lambda: None)
            self.assertEqual(len(store.listeners), 1)
            unsubscribe()
            self.assertEqual(len(store.listeners), 0)

        self.loop.run_until_complete(go())
