import inspect


def get_trace():
    stack = inspect.stack(0)
    for frame in stack[1:]:
        if frame.function == "<lambda>":
            continue
        if frame.function == "__init__":
            continue
        return frame
