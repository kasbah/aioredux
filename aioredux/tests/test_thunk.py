import toolz

import aioredux
import aioredux.middleware
import aioredux.utils
from aioredux.tests import base


class TestThunk(base.TestCase):

    def test_todo_thunk(self):
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

        thunk_middleware = aioredux.middleware.thunk_middleware
        create_store_with_middleware = aioredux.apply_middleware(thunk_middleware)(aioredux.Store)
        store = create_store_with_middleware(reducer, initial_state)

        self.assertIsNotNone(store.state)
        self.assertIsNotNone(store.state['todos'])
        self.assertEqual(len(store.state['todos']), 0)
        # use a thunk
        store.dispatch(lambda dispatch, state_func: dispatch(add_todo('todo text')))
        self.assertIsNotNone(store.state)
        self.assertIsNotNone(store.state['todos'])
        self.assertEqual(len(store.state['todos']), 1)
