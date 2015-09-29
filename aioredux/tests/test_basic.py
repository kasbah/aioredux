import toolz

import aioredux
from aioredux.tests import base


class TestAioredux(base.TestCase):

    def test_todo(self):
        initial_state = {
            'todos': (),
        }
        store = aioredux.Store(lambda state, action: state, initial_state)
        self.assertIsNotNone(store)
        self.assertIsNotNone(store.state)

    def test_todo_reducer(self):
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

        store = aioredux.Store(reducer, initial_state)
        self.assertIsNotNone(store.state)
        self.assertIsNotNone(store.state['todos'])
        self.assertEqual(len(store.state['todos']), 0)
        store.dispatch(add_todo('todo text'))
        self.assertIsNotNone(store.state)
        self.assertIsNotNone(store.state['todos'])
        self.assertEqual(len(store.state['todos']), 1)
