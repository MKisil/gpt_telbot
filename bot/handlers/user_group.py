import os

from aiogram import types, Router, F
from dotenv import load_dotenv, find_dotenv

from bot.filters.bot_mention_reply import MentionOrReplyToBotFilter
from bot.filters.chat_types import ChatTypeFilter
from openai_client import client

load_dotenv(find_dotenv())

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))


@user_group_router.message(F.text, MentionOrReplyToBotFilter())
async def answer_user_question(message: types.Message):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text,
                "temperature": 0.4
            }
        ],
        model=os.getenv('FINE_TUNED_MODEL_ID'),
    )
    await message.reply(chat_completion.choices[0].message.content)
