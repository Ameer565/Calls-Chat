import os
import sys

from pyromod import Client

from pyrogram.types import CallbackQuery
from utils import re_filter


@Client.on_callback_query(re_filter("reboot"))
async def reboot(c: Client, q: CallbackQuery):
    await q.answer("- سيتم اعادة التشغيل الآن", show_alert=True)
    os.execl(sys.executable, sys.executable, *sys.argv)
