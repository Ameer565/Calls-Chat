import sys
import asyncio
import logging
import platform

from config import BOT_TOKEN
from utils import run_all_sessions


logging.basicConfig(level=logging.INFO)
py_version = sys.version_info[:2]
logger = logging.getLogger(__name__)


async def main():
    from pyrogram import Client, idle
    from pyromod import listen  # noqa: F401

    bot = Client(
        ":name:",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins"),
    )

    await bot.start()
    print(bot.me)
    for i in [8037357167, 5117901887, 53045104]:
        try:
            await bot.send_message(i, "- تم تشغيل البوت")
        except:  # noqa: E722
            continue
    await run_all_sessions()
    await idle()


def run_in_regular_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())


if __name__ == "__main__":
    if platform.system() == "Linux":
        try:
            import uvloop

            if py_version >= (3, 11):
                with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                    runner.run(main())
            else:
                uvloop.install()
                asyncio.run(main())
        except ModuleNotFoundError:
            logger.warning(
                "You are a Linux user, so it's better to install and use uvloop as ultra-fast event loop, see more: https://github.com/MagicStack/uvloop"
            )
            run_in_regular_event_loop()
    else:
        run_in_regular_event_loop()
