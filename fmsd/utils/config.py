import inspect

from fmsd.utils.truecolor import truecolor


class Config:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        trace: bool = False,
        debug: bool = False,
        levels: int = 3,
    ) -> None:
        self.trace = trace
        self.debug = debug
        self.levels = levels

    def get_trace(self):
        if not self.trace:
            return None
        stack = inspect.stack(0)
        for frame in stack[1:]:
            if frame.function == "<lambda>":
                continue
            if frame.function == "__init__":
                continue
            return frame

    def truecolor(self, level: int, text: str) -> str:
        if level % 2 == 1:
            return text
        level //= 2
        brightness = min(255 // self.levels * (level // 3), 255)
        bg_buf = [0, 0, 0]
        bg_buf[level % 3] = 255
        bg_buf[(level + 1) % 3] = brightness
        bg_buf[(level + 2) % 3] = brightness
        fg = (255, 255, 255) if brightness < 128 and level != 1 else (0, 0, 0)
        return truecolor(fg, (bg_buf[0], bg_buf[1], bg_buf[2]), text)


config = Config()

__all__ = [
    "Config",
    "config",
]
