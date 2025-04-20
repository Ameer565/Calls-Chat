from pyromod import Client

from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode
from utils import re_filter, get_sessions


@Client.on_callback_query(re_filter("accounts"))
async def add_account(c: Client, q: CallbackQuery):
    await q.answer("- سيتم ارسال كل معلومات الحسابات لك الآن", show_alert=True)
    sessions = await get_sessions()
    if not sessions:
        return await q.message.reply("- لا يوجد اي حساب")
    text = "\n".join(f"+{i[4]} - {i[2]} - @{i[3]}" for i in sessions)
    splitted_text = [text[i : i + 4096] for i in range(0, len(text), 4096)]

    for i in splitted_text:
        await c.send_message(q.message.chat.id, i, parse_mode=ParseMode.DISABLED)
