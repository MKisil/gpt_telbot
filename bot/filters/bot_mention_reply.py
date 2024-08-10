from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.bot_client import bot


class MentionOrReplyToBotFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_username = (await bot.get_me()).username
        is_mention = ('@' + bot_username) in message.text.lower() if message.text else False
        is_reply = message.reply_to_message and message.reply_to_message.from_user.id == (await bot.get_me()).id
        return is_mention or is_reply
