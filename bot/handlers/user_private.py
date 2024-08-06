from aiogram import types, Router, F
from aiogram.filters import CommandStart

from openai_client import client

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привіт, я відповім на ваші запитання")


@user_private_router.message(F.text)
async def menu_cmd(message: types.Message):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text,
                "temperature": 0.4
            }
        ],
        model="gpt-4o-mini",
    )
    await message.answer(chat_completion.choices[0].message.content)
