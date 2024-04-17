from typing import NotRequired, TypedDict

__all__ = ('Button', 'KeyboardMarkup')


class Button(TypedDict):
    text: str
    url: NotRequired[str]
    callback_data: NotRequired[str]


class KeyboardMarkup(TypedDict):
    inline_keyboard: list[list[Button]]
