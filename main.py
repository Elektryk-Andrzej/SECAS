import discord
import discord.ext.commands
import time

from bot_main.info_embed import info_embed
from script_validator import VerdictHandler, LogHandler, IOHandlerVS, ParamHandler, ActionHandler, Utils, Data
from label_visualiser import IOHandlerVL
from tokens.discord_token import DISCORD_TOKEN
from shelp import IOHandlerSH
import command_prefixes as cmd

bot = discord.ext.commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def command_trigger(value: str, key: str) -> bool:
    return True if value.strip().casefold().startswith("." + key) else False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".i / .vs / .vl / .sh"),
        status=discord.Status.online
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return

    if (await command_trigger(message.content, cmd.info)
            or str(bot.user.id) in str(message.content)):
        await info_embed(message, bot)

    elif await command_trigger(message.content, cmd.visualise_labels):
        lv = IOHandlerVL.IOHandler(message, bot)
        await lv.visualise()

    elif await command_trigger(message.content, cmd.script_help):
        sh = IOHandlerSH.IOHandler(message)
        await sh.process_help_request()

    elif await command_trigger(message.content, cmd.verify_script):
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

        await data.io_handler_object.proccess_request()

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
            "Check `.i` for more info."
        )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
