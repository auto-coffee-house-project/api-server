__all__ = ('TelegramBotApiError',)


class TelegramBotApiError(Exception):
    """Raised when the Telegram Bot API returns an error."""

    def __init__(self, description: str):
        self.description = description
        super().__init__(f'Telegram Bot API error: {description}')
