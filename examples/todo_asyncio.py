import asyncio
import enum
import logging

import toolz

import aioredux
import aioredux.middleware

logger = logging.getLogger(__name__)


# action types
@enum.unique
class ActionTypes(enum.Enum):
    ADD_TODO = 1
    REMOVE_TODO = 2
    COMPLETE_TODO = 3


# action creators
def add_todo(text):
    return {'type': ActionTypes.ADD_TODO, 'text': text}


def complete_todo(index):
    return {'type': ActionTypes.COMPLETE_TODO, 'index': index}


def add_todo_slow():
    @asyncio.coroutine
    def thunk(dispatch, state_func=None):
        yield from asyncio.sleep(0.1)
        dispatch(add_todo('do task z1 (from coroutine)'))
        yield from asyncio.sleep(0.1)
        dispatch(add_todo('do task z2 (from coroutine)'))
    return thunk


# initial state
initial_state = {
    'todos': ()
}


# reducers
def todo_app(state, action):
    if action['type'] == ActionTypes.ADD_TODO:
        todos = state['todos'] + (action['text'],)
        return toolz.assoc(state, 'todos', todos)
    elif action['type'] == ActionTypes.COMPLETE_TODO:
        todos = state['todos'][:action['index']] + state['todos'][action['index'] + 1:]
        return toolz.assoc(state, 'todos', todos)
    else:
        return state


@asyncio.coroutine
def run():
    thunk_middleware = aioredux.middleware.thunk_middleware
    create_store_with_middleware = aioredux.apply_middleware(thunk_middleware)(aioredux.Store)
    store = create_store_with_middleware(todo_app, initial_state)

    store.subscribe(lambda: logging.info("new state: {}".format(store.state)))
    store.dispatch(add_todo_slow())
    for i in range(5):
        store.dispatch(add_todo('do task {}'.format(i)))
    store.dispatch(complete_todo(1))
    store.dispatch(complete_todo(2))
    yield from asyncio.sleep(0.5)
    logging.info('Finished')

if __name__ == '__main__':
    # configure logging
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
