from pyrsistent import pmap, pvector  # noqa

import aioredux
from aioredux.tests import base


class TestAioredux(base.TestCase):

    def test_todo(self):
        initial_state = pmap({
            'todos': pvector([])
        })
        store = aioredux.Store(lambda state, action: state, initial_state)
        self.assertIsNotNone(store)
