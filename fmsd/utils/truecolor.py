"""
https://github.com/termstandard/colors
"""

Color = tuple[int, int, int]


def truecolor(fg: Color, bg: Color, text: str) -> str:
    return "\x1b[48;2;{};{};{}m\x1b[38;2;{};{};{}m{}\x1b[0m".format(*bg, *fg, text)
