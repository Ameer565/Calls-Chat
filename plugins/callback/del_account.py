from pyromod import Client, Message

from pyrogram.types import CallbackQuery
from pyrogram import filters

from utils import re_filter, is_cancelled, delete_session, get_sessions


@Client.on_callback_query(re_filter("del account"))
async def delete_account(c: Client, q: CallbackQuery):
    await q.message.reply("- ارسل رقم الهاتف الان")

    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)

    if await is_cancelled(ask):
        return

    phone_number = ask.text.strip().replace("+", "").replace(" ", "")

    for session in await get_sessions():
        if session[4] == phone_number:
            await delete_session(session)
            return await ask.reply("- تم حذف الرقم بنجاح")

    return await ask.reply("- هذا الرقم غير موجود")
