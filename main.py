import discord
import discord.ext.commands
import time

from bot_main.info_embed import info_embed
from script_validator import VerdictHandler, LogHandler, IOHandlerVS, ParamHandler, ActionHandler, Utils, Data
from label_visualiser import IOHandlerVL
from tokens.discord_token import DISCORD_TOKEN
from shelp import IOHandlerSH, update_shelp_files
from easter_eggs import reply_vid
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
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return

    if await command_trigger(msg.content, cmd.info):
        await info_embed(msg, bot)
        return

    if msg.author.id == 762016625096261652 and await command_trigger(msg.content, "ush"):
        try:
            await update_shelp_files.update_variables()
            await msg.channel.send("Updated variables")

            await update_shelp_files.update_actions()
            await msg.channel.send("Updated actions")

        except Exception as e:
            await msg.reply(f"There has been an exception while updating shelp\n\t{e}")

        else:
            await msg.reply("Everything has been updated!")

        return

    if await command_trigger(msg.content, cmd.visualise_labels):
        lv = IOHandlerVL.IOHandler(msg, bot)
        await lv.visualise()
        return

    if await command_trigger(msg.content, cmd.script_help):
        sh = IOHandlerSH.IOHandler(msg)
        await sh.process_help_request()
        return

    if await command_trigger(msg.content, cmd.verify_script):
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

        data.io_handler_object = IOHandlerVS.IOHandler(data, msg, bot)

        """try:"""

        await data.io_handler_object.proccess_request()

        """except Exception as e:
            await message.reply(f"ERROR: `{e}`")

            with open(data.log_file_name, "rb") as file:
                # noinspection PyTypeChecker
                await message.channel.send(file=discord.File(file, "result.txt"))"""
        return

    if await command_trigger(msg.content, "v"):
        await msg.reply(
            "Prefix `.v` is no longer supported\n"
            "Check `.i` for more info."
        )
        return

    if "sex" in msg.content.casefold():
        await reply_vid.bomb_them(msg)
        return

    if msg.mentions and len(msg.mentions) == 1:
        member: discord.Member = msg.mentions[0]
        beanz_id: int = 762016625096261652
        andrzej_id: int = 703301663049384058

        if member.id == andrzej_id and msg.author.id == beanz_id:
            await reply_vid.kissmass(msg)
            return


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
