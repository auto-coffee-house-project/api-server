from typing import TypedDict

__all__ = ('Button', 'KeyboardMarkup')


class Button(TypedDict):
    text: str
    url: str


class KeyboardMarkup(TypedDict):
    inline_keyboard: list[list[Button]]
