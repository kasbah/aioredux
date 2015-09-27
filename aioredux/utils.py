import collections.abc

import toolz

import aioredux


def apply_middleware(*middlewares):
    def next_func(next):
        def create_store(reducer, initial_state=None):
            store = aioredux.Store(reducer, initial_state)
            dispatch = store.dispatch
            middleware_api = dict(dispatch=dispatch, state_func=lambda: store.state)
            chain = map(lambda middleware: middleware(**middleware_api), middlewares)
            store.dispatch = toolz.compose(*chain)(dispatch)
            return store
        return create_store
    return next_func


def is_mapping(action):
    '''Analogous to isPlainObject'''
    return isinstance(action, collections.abc.Mapping)


def is_FSA(action):
    '''Checks whether `action` is a Flux Standard Action (FSA).'''
    if not is_mapping(action):
        return False
    if 'type' not in action:
        return False
    properties = {'type', 'action', 'payload', 'error', 'meta'}
    if len(action.keys() - properties) > 0:
        return False
    if not is_mapping(action.get('payload', {})):
        return False
    return True
