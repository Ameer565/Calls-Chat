from pyromod import Client, Message
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(
    filters.command("start")
    & filters.private
    & filters.user([8037357167, 5117901887, 53045104])
)
async def on_start_command(bot: Client, m: Message) -> Message:
    await m.react("❤️", big=True)
    return await m.reply_text(
        "- اختر ما تريده من الازرار",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اضافة حساب", callback_data="add account"),
                    InlineKeyboardButton("حذف حساب", callback_data="del account"),
                ],
                [
                    InlineKeyboardButton("انضمام لمكالمة", callback_data="play call"),
                    InlineKeyboardButton("مغادرة مكالمة", callback_data="leave call"),
                ],
                [
                    InlineKeyboardButton("انضمام لدردشة", callback_data="join chat"),
                    InlineKeyboardButton("مغادرة دردشة", callback_data="leave chat"),
                ],
                [
                    InlineKeyboardButton("الحسابات", callback_data="accounts"),
                    InlineKeyboardButton("اعادة تشغيل", callback_data="reboot"),
                ],
            ]
        ),
    )
