import asyncio


def thunk_middleware(dispatch, state_func):
    def next_func(next_handler):
        def action_func(action):
            if asyncio.iscoroutine(action):
                raise RuntimeError('Expected coroutine function, found coroutine: {}'.format(action))
            if callable(action):
                return action(dispatch, state_func)
            else:
                return next_handler(action)
        return action_func
    return next_func
