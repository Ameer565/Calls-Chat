import json
import os
import random
import kvsqlite

from asyncio import create_subprocess_shell, subprocess
from typing import List, Union

from pyrogram import filters
from pyrogram.types import Message

db: kvsqlite.Client = None


def re_filter(_: str) -> filters.Filter:
    return filters.regex(rf"^{_}$")


def get_db() -> kvsqlite.Client:
    global db
    if db is not None:
        return db
    db = kvsqlite.Client("accounts.db")
    return db


async def is_cancelled(m: Message):
    if m.text == "الغاء":
        await m.reply("- تم الالغاء", quote=True)
        return True

    return False


async def exec_shell(cmd: str) -> None:
    sh = await create_subprocess_shell(
        cmd=cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    print(await sh.wait(), cmd)


async def get_sessions() -> List[List[Union[str, int]]]:
    return await get_db().get("sessions") or []


async def insert_session(session: str):
    sessions = await get_sessions()
    sessions.append(session)
    await get_db().set("sessions", sessions)


async def delete_session(session: str):
    sessions = await get_sessions()
    sessions.remove(session)
    await get_db().set("sessions", sessions)


async def run_all_sessions():
    await exec_shell("pm2 kill")

    all_sessions = [i[0] for i in await get_sessions()]

    if not all_sessions:
        return

    sessions_20 = [all_sessions[i : i + 20] for i in range(0, len(all_sessions), 20)]

    for sessions in sessions_20:
        os.environ.update({"sessions": json.dumps(sessions, ensure_ascii=False)})

        process_id = random.randint(1, 99999)
        await exec_shell(f"pm2 start run.py --name b{process_id} --no-autorestart")

    await exec_shell("pm2 save")
    del os.environ["sessions"]
    print("Done")
