import asyncio
import json
import logging


logger = logging.getLogger(__name__)


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


def logger_middleware(dispatch, state_func):
    def next_func(next_handler):
        def action_func(action):
            logger.info('PREV STATE: {}'.format(json.dumps(state_func())))
            logger.info('ACTION: {}'.format(json.dumps(action)))
            val = next_handler(action)
            logger.info('NEW STATE: {}'.format(json.dumps(state_func())))
            return val
        return action_func
    return next_func
