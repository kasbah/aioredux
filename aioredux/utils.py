import collections.abc

import toolz

try:
    from types import coroutine
except ImportError:
    from asyncio import coroutine


def apply_middleware(*middlewares):
    def next_func(next_handler):
        # next_ is typically aioredux.create_store
        @coroutine
        def create_store(reducer, initial_state=None):
            store = yield from next_handler(reducer, initial_state)
            dispatch = store.dispatch
            middleware_api = dict(dispatch=lambda action: store.dispatch(action), state_func=lambda: store.state)
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
    return True


def combine_reducers(reducers):
    assert all(callable(val) for val in reducers.values())
    default_state = {k: None for k in reducers}

    def combination(state=None, action=None):
        if state is None:
            state = default_state
        has_changed = False

        def next_state(key, reducer):
            nonlocal has_changed
            previous_state_for_key = state[key]
            next_state_for_key = reducer(previous_state_for_key, action)
            if next_state_for_key is None:
                msg = ('`None` is not an allowed initial state when using `combine_reducers`. '
                       '`None` is used to indicate a malfunctioning reducer initialization.')
                raise ValueError(msg)
            has_changed |= next_state_for_key is not previous_state_for_key
            return next_state_for_key
        final_state = {key: next_state(key, reducer) for key, reducer in reducers.items()}
        return final_state if has_changed else state
    return combination
