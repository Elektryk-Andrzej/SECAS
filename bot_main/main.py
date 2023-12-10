import discord
import discord.ext.commands
import os
import time

from bot_main.info_embed import info_embed
from script_validator import VerdictHandler, LogHandler, IOHandlerVS, ParamHandler, ActionHandler, Utils, Data
from label_visualiser import IOHandlerVL
from tokens.discord_token import DISCORD_TOKEN

bot = discord.ext.commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def command_trigger(value: str, key: str) -> bool:
    return True if value.strip().casefold().startswith("." + key) else False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".v / .i"),
        status=discord.Status.online
    )


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if await command_trigger(message.content, "i") or str(bot.user.id) in str(message.content):
        await info_embed(message, bot)

    elif await command_trigger(message.content, "vl"):
        lv = IOHandlerVL.IOHandler(message, bot)
        await lv.visualise()

    elif await command_trigger(message.content, "vs"):
        data = Data.Data()
        time.sleep(.1)

        data.log_handler_object = LogHandler.LogHandler(data)
        time.sleep(.1)

        data.utils_object = Utils.Utils(data)
        time.sleep(.1)

        data.verdict_handler_object = VerdictHandler.VerdictHandler(data)
        time.sleep(.1)

        data.param_handler_object = ParamHandler.ParamHandler(data)
        time.sleep(.1)

        data.action_handler_object = ActionHandler.ActionHandler(data)
        time.sleep(.1)

        data.io_handler_object = IOHandlerVS.IOHandler(data, message, bot)

        """try:"""
        if os.path.exists(f".\\Logs\\{data.log_file_name}"):
            await message.reply("Calm down!", mention_author=False)

        count_first_line: bool
        if message.attachments and message.attachments[0].filename.endswith('.txt'):
            attachment = message.attachments[0]
            message_content = await attachment.read()
            data.code = message_content.decode("utf-8")
            count_first_line = True
        else:
            data.code = message.content
            count_first_line = False

        await data.io_handler_object.proccess_verify_request(count_first_line=count_first_line)

        if await command_trigger(message.content, "vsd"):
            with open(data.log_file_name, "rb") as file:
                # noinspection PyTypeChecker
                await message.channel.send(file=discord.File(file, "result.txt"))

        """except Exception as e:
            await message.reply(f"ERROR: `{e}`")

            with open(data.log_file_name, "rb") as file:
                # noinspection PyTypeChecker
                await message.channel.send(file=discord.File(file, "result.txt"))"""

    elif await command_trigger(message.content, "v"):
        await message.reply(
            "Prefix `.v` is no longer supported\n"
            "Use `.vs` to verify script\n"
            "Use `.vl` to visualise labels"
        )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
