from pyromod import Client, Message

from pyrogram.types import CallbackQuery
from pyrogram import filters, errors
from utils import re_filter, is_cancelled, insert_session


@Client.on_callback_query(re_filter("add account"))
async def add_account(c: Client, q: CallbackQuery):
    await q.message.reply("- ارسل الآن رقم هاتف الحساب : ", True)
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)

    if await is_cancelled(ask):
        return

    rep = await ask.reply("- يتم ارسال الكود الان", quote=True)
    phone_number = ask.text

    try:
        from pyrogram import Client

        client = Client(
            "name", 13251350, "66c0eacb36f9979ae6d153f207565cd6", in_memory=True
        )
        await client.connect()
        code = await client.send_code(phone_number)
    except Exception as e:
        return await rep.edit_text(f"- حدث خطأ: \n\n```sh\n{e}\n```")

    await rep.edit_text("- ارسل كود تسجيل الدخول الآن")
    ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)
    if await is_cancelled(ask):
        return
    try:
        await client.sign_in(phone_number, code.phone_code_hash, ask.text)
    except errors.SessionPasswordNeeded:
        await q.message.reply("- ارسل كلمة سر التحقق بخطوتين الان: ", True)
        ask: Message = await c.ask(q.message.chat.id, "", filters=filters.text)
        if await is_cancelled(ask):
            return
        try:
            await client.check_password(ask.text)
        except Exception as e:
            return await ask.reply(f"- حدث خطأ: \n\n```sh\n{e}\n```", True)
    except Exception as e:
        return await ask.reply(f"- حدث خطأ: \n\n```sh\n{e}\n```", True)

    session = await client.export_session_string()
    me = await client.get_me()
    await insert_session([session, me.id, me.first_name, me.username, me.phone_number])
    return await ask.reply(
        "- تم اضافة الحساب بنجاح ولكن لن يتم تشغيله, في حال اردت تشغيل كل الحسابات المضافة عليك اعادة تشغيل البوت, كن حذرًا فالافضل ان تعيد تشغيله عندما تنتهي نمن اضافة كل الحسابات لكي تشغلهم مع بعض, تجنبًا للحظر"
    )
