import unittest
from unittest.mock import AsyncMock

from constants.constants import (
    GREETING_ANSWER, COMMAND_LIST,
    BYE_ANSWER, HASBIK_HELLO, BYE_STICKER, UNKNOWN_ANSWER,
    UNKNOWN_STICKER, NON_TYPE_ANSWER, NON_TYPE_STICKER
)
from handlers.user_private import (
    start_cmd, help_cmd,
    hello_cmd, stub, bye_cmd
)
from keyboard.inline import git
from keyboard.reply import start_keyboard


class TestBaseHandler(unittest.IsolatedAsyncioTestCase):
    """
        Тестирование базовых хэндлеров.
        Для вызова тестов, использовать команду
        в терминале: python -m unittest
     """

    async def test_start_handler(self):
        """Тестирование хэндлера на обработку команды /start"""
        message = AsyncMock()
        await start_cmd(message)
        message.answer.assert_called_with(
            f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER,
            reply_markup=start_keyboard
        )
        message.answer_animation.assert_called_with(HASBIK_HELLO)

    async def test_hello_handler(self):
        """Тестирование хэндлера на обработку команды /hello"""
        message = AsyncMock()
        await hello_cmd(message)
        message.reply.assert_called_with(
            f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER
        )
        message.answer_animation.assert_called_with(HASBIK_HELLO)

    async def test_hello_word(self):
        """Тестирование хэндлера на обработку команды 'привет'"""
        message = AsyncMock()
        message.from_user.first_name = "TestUser"
        message.text = "привет"
        await hello_cmd(message)
        message.reply.assert_called_with(
            f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER
        )
        message.answer_animation.assert_called_with(HASBIK_HELLO)

    async def test_help_handler(self):
        """Тестирование хэндлера на обработку команды /help"""
        message = AsyncMock()
        await help_cmd(message)
        message.answer.assert_called_with(
            f'<b>{message.from_user.first_name}</b> \n'
            f'{COMMAND_LIST}',
            reply_markup=git
        )

    async def test_bye_handler(self):
        """Тестирование хэндлера на обработку команды /bye"""
        message = AsyncMock()
        await bye_cmd(message)
        message.reply.assert_called_with(
            BYE_ANSWER + f'<b>{message.from_user.first_name}</b>!'
        )
        message.answer_animation.assert_called_with(BYE_STICKER)

    async def test_bye_word(self):
        """Тестирование хэндлера на обработку команды 'пока'"""
        message = AsyncMock()
        message.from_user.first_name = "TestUser"
        message.text = "пока"
        await bye_cmd(message)
        message.reply.assert_called_with(
            BYE_ANSWER + f'<b>{message.from_user.first_name}</b>!'
        )
        message.answer_animation.assert_called_with(BYE_STICKER)

    async def test_stub(self):
        """Тестирование хэндлера на обработку неизвестной команды"""
        message = AsyncMock()
        message.from_user.first_name = "TestUser"
        message.text = "/unknown_command"
        await stub(message)
        message.answer.assert_called_with(
            UNKNOWN_ANSWER + f'<b>{message.text}</b>\n' + COMMAND_LIST
        )
        message.answer_animation.assert_called_with(UNKNOWN_STICKER)

    async def test_non_text_message(self):
        """Тестирование хэндлера на обработку не текстового сообщения"""
        message = AsyncMock()
        message.from_user.first_name = "TestUser"
        message.text = None
        await stub(message)
        message.answer.assert_called_with(NON_TYPE_ANSWER)
        message.answer_animation.assert_called_with(NON_TYPE_STICKER)


if __name__ == "__main__":
    unittest.main()
