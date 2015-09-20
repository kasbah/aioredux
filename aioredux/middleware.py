import asyncio


def thunk_middleware(dispatch, state_func):
    def next_func(next):
        def action_func(action):
            if callable(action):
                if asyncio.iscoroutinefunction(action):
                    # asyncio.async renamed to asyncio.ensure_future in py>=3.4.4
                    asyncio.async(action(dispatch, state_func))
                else:
                    action(dispatch, state_func)
            else:
                next(action)
        return action_func
    return next_func
