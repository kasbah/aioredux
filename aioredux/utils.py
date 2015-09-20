import toolz

import aioredux


def apply_middleware(*middlewares):
    def next_func(next):
        def create_store(reducer, initial_state):
            store = aioredux.Store(reducer, initial_state)
            dispatch = store.dispatch
            middleware_api = dict(dispatch=dispatch, state_func=lambda: store.state)
            chain = map(lambda middleware: middleware(**middleware_api), middlewares)
            store.dispatch = toolz.compose(*chain)(dispatch)
            return store
        return create_store
    return next_func
