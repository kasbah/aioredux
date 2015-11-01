import asyncio


def thunk_middleware(dispatch, state_func):
    def next_func(next_):
        def action_func(action):
            if callable(action):
                if not asyncio.iscoroutinefunction(action):
                    raise RuntimeError('thunk must be a coroutine')
                return action(dispatch, state_func)
            else:
                return next_(action)
        return action_func
    return next_func
