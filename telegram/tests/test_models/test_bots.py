from telegram.models import Bot


def test_bot_str() -> None:
    bot = Bot(name='test_bot')
    assert str(bot) == bot.name
