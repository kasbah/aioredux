import enum

import aioredux.utils


class ActionTypes(enum.Enum):
    INIT = '@@redux/INIT'


class Store:
    '''Creates a store which holds the state tree.'''

    def __init__(self, reducer, initial_state=None):
        if not callable(reducer):
            raise ValueError('Expected the reducer to be callable.')
        self.reducer = reducer
        self._state = initial_state
        self.listeners = set()
        self.is_dispatching = False

        # dispatch an 'INIT' action so every reducer returns initial state
        self.dispatch({'type': ActionTypes.INIT})

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

    def replace_reducer(self, next_reducer):
        self.reducer = next_reducer
        self.dispatch({'type': ActionTypes.INIT})

    def dispatch(self, action):
        '''Dispatch an action.'''
        if not aioredux.utils.is_mapping(action):
            return ValueError('Actions must be mappings.')
        if self.is_dispatching:
            return RuntimeError('Reducers may not dispatch actions.')
        try:
            self.is_dispatching = True
            next_state = self.reducer(self.state, action)
        finally:
            self.is_dispatching = False
        # If no change in state, do not notify subscribers
        if next_state != self.state:
            self._state = next_state
            for listener in self.listeners:
                listener()
        return action
