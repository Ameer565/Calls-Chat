import uvloop
import asyncio
import json
import os
import sys
import logging
import redis.asyncio as redis

from pyrogram import Client
from pytgcalls import PyTgCalls

from typing import List, Tuple, Union

clients: List[Tuple[Client, PyTgCalls]] = []
logger = logging.getLogger(__name__)


async def play(chat_id: Union[int, str], id: int, number: int, r: redis.Redis):
    for _, call in clients:
        if len(await r.smembers(str(id))) >= number:
            break
        try:
            await call.play(chat_id)
            await call.mute_stream(chat_id)
            await r.sadd(str(id), str(_.me.id))
            await asyncio.sleep(1)
        except Exception as e:
            print(e.__class__.__name__ + ": " + str(e))


async def leave(chat_id: Union[int, str]):
    for _, call in clients:
        try:
            await call.leave_call(chat_id)
        except Exception as e:
            print(e.__class__.__name__ + ": " + str(e))


async def join(chat_link: str, id: int, number: int, r: redis.Redis):
    for client, _ in clients:
        if len(await r.smembers(str(id))) >= number:
            break
        try:
            await client.join_chat(chat_link)
            await r.sadd(str(id), str(client.me.id))
            await asyncio.sleep(1)
        except Exception as e:
            print(e.__class__.__name__ + ": " + str(e))


async def leave_g(chat_id: Union[int, str]):
    for client, _ in clients:
        try:
            await client.leave_chat(chat_id)
        except Exception as e:
            print(e.__class__.__name__ + ": " + str(e))


async def task():
    done: List[int] = []
    r = redis.Redis(decode_responses=True)
    while not await asyncio.sleep(2.5):
        todo = await r.get("todo")
        if todo is None:
            continue

        todo = json.loads(todo)

        if todo["id"] in done:
            continue

        print("Found something to do: ", todo)
        try:
            if todo["command"] == "leave":
                warning = "Leaving the VC from the chat: " + str(todo["chat_id"])
                await leave(todo["chat_id"])
            elif todo["command"] == "leave_g":
                warning = "Leaving the chat: " + str(todo["chat_id"])
                await leave_g(todo["chat_id"])
            elif todo["command"] == "play":
                warning = "Joining the VC in the chat: " + str(todo["chat_id"])
                await play(todo["chat_id"], todo["id"], todo["number"], r)
            elif todo["command"] == "join":
                warning = "Joining the chat: " + todo["link"]
                await join(todo["link"], todo["id"], todo["number"], r)
        except:  # noqa: E722
            pass

        done.append(todo["id"])

        logger.warning(warning)


async def main():
    sessions = os.environ.get("sessions")
    print(sessions)
    if sessions is None:
        sys.exit()

    sessions = json.loads(sessions)
    for session in sessions:
        try:
            client = Client("name", session_string=session, workers=1)
            call = PyTgCalls(client, 1)
            await call.start()
            clients.append((client, call))
        except:  # noqa: E722
            continue

    if not clients:
        sys.exit()

    await asyncio.create_task(task())


if __name__ == "__main__":
    if sys.version_info[:2] >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
