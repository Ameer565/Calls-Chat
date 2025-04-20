import json
import random
import redis.asyncio as redis

from pyromod import Client, Message

from pyrogram.types import CallbackQuery
from pyrogram import filters

from utils import re_filter, is_cancelled, get_sessions


@Client.on_callback_query(re_filter("join chat"))
async def join_chat(c: Client, q: CallbackQuery):
    await q.message.reply("- ارسل الآن يوزر او رابط الدردشة: ", True)
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)
    if await is_cancelled(ask):
        return
    answer = ask.text.replace("@", "")

    await ask.reply(
        f"- ارسل الان عدد الحسابات المطلوب\n- عدد الحسابات الحالية : {len(await get_sessions())}"
    )
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)

    if not ask.text.isdigit():
        return await ask.reply("- عدد غير صحيح")

    number = int(ask.text)

    command = "join"

    r = redis.Redis(decode_responses=True)

    await r.set(
        "todo",
        json.dumps(
            {
                "command": command,
                "link": answer,
                "id": random.randint(999, 99999),
                "number": number,
            }
        ),
        ex=600,
    )

    await ask.reply(f"- تم ارسال الامر ل {number} حساب", quote=True)
