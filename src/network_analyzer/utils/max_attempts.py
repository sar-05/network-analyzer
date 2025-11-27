from functools import wraps
from types import FunctionType

import logging

logger = logging.getLogger(__name__)


class AttemptError(Exception):
    """Raise when max attempts reached."""


class MaxAttemptError(Exception):
    """Raise when max attempts are reached."""


def max_attempts(
    max_attempts: int = 5,
    input_param: str = "user_input",
    prompt: str = "Test input: ",
):
    def execute_attempts(func: FunctionType):
        @wraps(func)
        def wrap_attempts(*args, **kwargs):
            for _ in range(max_attempts):
                func_input = input(prompt)
                try:
                    # Inject inpur_param keyword argument
                    kwargs[input_param] = func_input
                    return func(*args, **kwargs)
                except AttemptError:
                    logger.warning("Missed attempt for %s", func.__name__)
                    continue
            logger.error("Max attempts {max_attempts} to execute %s", func.__name__)
            msg = f"Max attempts {max_attempts} to execute {func.__name__}"
            raise MaxAttemptError(msg)

        return wrap_attempts

    return execute_attempts
