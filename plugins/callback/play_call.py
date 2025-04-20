import redis.asyncio as redis
import json
import random

from pyromod import Client, Message

from pyrogram.types import CallbackQuery
from pyrogram import filters

from utils import re_filter, is_cancelled, get_sessions


@Client.on_callback_query(re_filter("play call"))
async def play_call(c: Client, q: CallbackQuery):
    await q.message.reply("- ارسل الآن يوزر او ايدي الدردشة: ", True)
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)
    if await is_cancelled(ask):
        return
    answer = ask.text.replace("-", "")

    if answer.isdigit():
        chat_id = int(ask.text)
    else:
        chat_id = ask.text.replace("@", "")

    await ask.reply(
        f"- ارسل الان عدد الحسابات المطلوب\n- عدد الحسابات الحالية : {len(await get_sessions())}"
    )
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)

    if not ask.text.isdigit():
        return await ask.reply("- عدد غير صحيح")

    number = int(ask.text)

    command = "play"

    r = redis.Redis(decode_responses=True)

    await r.set(
        "todo",
        json.dumps(
            {
                "command": command,
                "chat_id": chat_id,
                "id": random.randint(999, 99999),
                "number": number,
            }
        ),
        ex=600,
    )

    await ask.reply(f"- تم ارسال الامر ل {number} حساب", quote=True)
