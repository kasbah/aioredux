import aioredux
from aioredux.tests import base


class TestAioredux(base.TestCase):

    def test_todo(self):
        initial_state = {
            'todos': (),
        }
        store = aioredux.Store(lambda state, action: state, initial_state)
        self.assertIsNotNone(store)
