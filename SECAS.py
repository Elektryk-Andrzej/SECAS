import discord
import discord.ext.commands
from discord.ext import commands

import bot_variables
# import asyncio
from DO_NOT_SHIP.TOKEN import TOKEN
import re
from discord.utils import get
from CodeVerifier import VerifyCode

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"errorless code B)"),
        status=discord.Status.online)


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.content.startswith(".i") or message.content.startswith(".I"):
        print(f"{message.author} requested info")
        embed = discord.Embed(title=None,
                              description=None,
                              color=0xe84d97)

        embed.add_field(
            name=f"What is {bot.user.name}?",
            value="**Scripted Events Code Analysis System** "
                  "is a bot that allows you to easily check if your code has been constructed propperly.\n"
                  f"If a bug is found, {bot.user.name} will specify the place and the reason of the bug, helping "
                  f"you with fixing the error.\n",
            inline=False
        )
        embed.add_field(
            name=f"How to use {bot.user.name}?",
            value="It's very simple! Just write `.v` and put all of your code below. E.g.\n"
                  "```\n"
                  ".v\n"
                  "SETROLE * ClassD\n"
                  "HINTPLAYER {CLASSD} 6 You have 45 seconds of life left!\n"
                  "WAITSEC 45\n"
                  "KILL {CLASSD} Exploded```\n",
            inline=False
        )

        embed.add_field(
            name=f"What {bot.user.name} isn't capable of?",
            value=f"{bot.user.name} isn't capable of finding errors that are **logic** and **loop** related.\n"
                  f"If your code is still not working after verifying it with {bot.user.name}, explain your issue in "
                  f"<#1072723950456541245> and someone will help you fix it.",
            inline=False
        )

        embed.add_field(
            name=f"What should I do when I encounter a {bot.user.name} bug?",
            value=f"Just ping <@762016625096261652> and explain the bug. \n"
                  f"If you do that enough times, as special thanks you will be granted a place in this embed "
                  f"as a contributor!",
            inline=False
        )

        embed.add_field(
            name=f"{bot.user.name} project contributors!",
            value=f"`elektryk_andrzej` - Developer\n"
                  f"`saskyc` - Betatester",
            inline=False
        )
        await message.reply(embed=embed, mention_author=False)
        return

    elif message.content.startswith(".v") or message.content.startswith(".V"):
        print(f"{message.author} requested code verification")
        script = VerifyCode(message)

        async with message.channel.typing():
            try:
                script.code = message.content.split("\n")

                for index, line in enumerate(script.code):
                    if index == 0:
                        continue

                    script.line_processing_list = line.split(" ")
                    script.line_processing_list[-1].strip("\n")

                    if ":" in (iterator := script.line_processing_list[-1]):
                        script.iterators.append(iterator.strip(":"))

                for index, line in enumerate(script.code):
                    if index == 0:
                        continue

                    script.line_processing_index = index
                    script.line_processing_str = line.strip("\n")
                    script.line_processing_list = line.split(" ")
                    script.line_processing_list[-1].strip("\n")
                    script.line_already_added_to_result = False

                    '''for position, argument in enumerate(script.line_processing_list):
                        if argument == "":
                            await script.add_line_to_result("🟥")
                            await script.error_template(position, "Invalid space character | Delete it",
                                                        link=None)
                            script.errored = True'''

                    if (action_name := script.line_processing_list[0]) in script.actions:
                        action_done = await script.actions[action_name]()

                        if action_done:
                            await script.add_line_to_result("🟩")
                        else:
                            await script.add_line_to_result("🟥")
                            script.errored = True

                    elif "#" in script.line_processing_list[0]:
                        await script.add_line_to_result("🟦")

                    elif all(znak.isspace() for znak in script.line_processing_list) or \
                            script.line_processing_list == ['']:
                        await script.add_line_to_result("⬛")

                    elif ":" in script.line_processing_list[-1]:
                        await script.add_line_to_result("🟪")

                    elif "!--" in script.line_processing_list[0]:
                        await script.add_line_to_result("⬜")

                    else:
                        await script.add_line_to_result("🟥")
                        await script.error_template(0, "Invalid action | Find all here",
                                                    link="https://pastebin.com/6C0ry80E")

                        script.errored = True

                await script.send_result_embed()

            except Exception as e:
                await message.reply("An error occured while generating the overviev.\n"
                                    "<@762016625096261652> kurwa ruszaj dupę i chodź tu "
                                    "bo znowu się zjebałem przez to jak żeś okropnie mnie napisał.\n"
                                    f"`{e}`")
        del script

    elif message.content == "qwerty" and message.author.id == 762016625096261652:
        role_id = 846021698603319336
        for member in message.guild.members:
            for role in member.roles:
                if role.id == role_id:
                    role = get(message.guild.roles, id=role_id)

                    print(f"{member.name} posiada rolę {role}")

                    await member.send(f"Hi! I see that you have a role `{role.name}` in the {message.guild.name}!")


bot.run(TOKEN)
