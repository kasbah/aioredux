import asyncio
import enum
import logging

import aioredux
from pyrsistent import pmap, pvector  # noqa

logger = logging.getLogger(__name__)


# action types
class ActionTypes(enum.Enum):
    ADD_TODO = 1
    REMOVE_TODO = 2
    COMPLETE_TODO = 3


# action creators
def add_todo(text):
    return {'type': ActionTypes.ADD_TODO, 'text': text}


def complete_todo(index):
    return {'type': ActionTypes.COMPLETE_TODO, 'index': index}


# initial state
initial_state = pmap({
    'todos': pvector([])
})


# reducers
def todo_app(state, action):
    if action['type'] == ActionTypes.ADD_TODO:
        todos = state['todos'].append(action['text'])
        return state.update({'todos': todos})
    else:
        return state


@asyncio.coroutine
def run():
    store = aioredux.Store(todo_app, initial_state)
    store.subscribe(lambda: logging.info("new state: {}".format(store.state)))
    for i in range(5):
        store.dispatch(add_todo('do task {}'.format(i)))
    store.dispatch(complete_todo(3))
    logging.info('Finished')

if __name__ == '__main__':
    # configure logging
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
