import asyncio

import aioredux.utils

try:
    from types import coroutine
except ImportError:
    from asyncio import coroutine


class ActionTypes:
    INIT = '@@redux/INIT'


class Store:
    '''Creates a store which holds the state tree.'''

    def __init__(self, reducer, initial_state=None, loop=None):
        '''Do not call directly, use create_store'''
        if not callable(reducer):
            raise ValueError('Expected the reducer to be callable.')
        self.reducer = reducer
        self._state = initial_state
        self.listeners = set()
        self.is_dispatching = False
        self.loop = loop

    @property
    def state(self):
        '''Access current state (read-only).'''
        return self._state

    def subscribe(self, listener):
        '''Add a change listener.

        `listener` is a function which will be called when the state
        tree has changed.
        '''
        self.listeners.add(listener)

        def unsubscribe():
            self.listeners.remove(listener)

        return unsubscribe

    @coroutine
    def replace_reducer(self, next_reducer):
        self.reducer = next_reducer
        yield from self.dispatch({'type': ActionTypes.INIT})

    @coroutine
    def dispatch(self, action):
        '''Dispatch an action.'''
        if not aioredux.utils.is_mapping(action):
            if action is None:
                raise ValueError('Actions must be mappings, got `None`. Did you mean to return a thunk?')
            raise ValueError('Actions must be mappings, got: {}'.format(action))
        if self.is_dispatching:
            raise RuntimeError('Reducers may not dispatch actions.')
        try:
            self.is_dispatching = True
            next_state = self.reducer(self.state, action)
        finally:
            self.is_dispatching = False
        # If no change in state, do not notify subscribers
        if next_state is not self.state:
            self._state = next_state
            for listener in self.listeners:
                listener()
        future = asyncio.Future(loop=self.loop)
        future.set_result(action)
        return future


@coroutine
def create_store(*args, **kwargs):
    store = Store(*args, **kwargs)
    # dispatch an 'INIT' action so every reducer returns initial state
    yield from store.dispatch({'type': ActionTypes.INIT})
    return store
