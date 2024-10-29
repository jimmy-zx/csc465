import inspect

from fmsd.utils.config import config


def get_trace():
    if not config.trace:
        return None
    stack = inspect.stack(0)
    for frame in stack[1:]:
        if frame.function == "<lambda>":
            continue
        if frame.function == "__init__":
            continue
        return frame


__all__ = [
    "get_trace",
]
