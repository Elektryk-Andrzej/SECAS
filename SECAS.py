import discord
import discord.ext.commands
from discord.ext import commands

from DO_NOT_SHIP.TOKEN import TOKEN
from discord.utils import get
from CodeVerifier import VerifyCode

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def proccess_verify_request(script):
    async with (script.ctx.channel.typing()):
        try:
            # register all labels
            for index, line in enumerate(script.code):
                script.line_processing_list = line.split(" ")
                script.line_processing_list[-1].strip("\n")
                if index == 0 and len(script.line_processing_list) > 1 and\
                        script.line_processing_list[0].startswith("."):

                    script.line_processing_list.pop(0)

                if ":" in (label := script.line_processing_list[-1]):
                    script.labels.append(label.strip(":"))

            # for all lines to be verified
            for index, line in enumerate(script.code):
                script.line_processing_index = index
                script.line_processing_str = line.strip("\n")
                script.line_processing_list = line.split(" ")
                script.line_processing_list[-1].strip("\n")
                script.line_already_added_to_result = False

                # delete .v from the first line
                if index == 0 and len(script.line_processing_list) > 1 and\
                        script.line_processing_list[0].startswith("."):

                    script.line_processing_str = script.line_processing_str.strip(
                        f"{script.line_processing_list[0]} ")
                    script.line_processing_list.pop(0)

                '''for position, argument in enumerate(script.line_processing_list):
                    if argument == "":
                        await script.add_line_to_result("🟥")
                        await script.error_template(position, "Invalid space character | Delete it",
                                                    link=None)
                        script.errored = True'''

                # run check for action if exists
                if (action_name := script.line_processing_list[0]) in script.actions:
                    action_done = await script.actions[action_name]()

                    if action_done:
                        await script.add_line_to_result("🟩")
                    else:
                        await script.add_line_to_result("🟥")
                        script.errored = True

                # = comments, so change color for em
                elif "#" in script.line_processing_list[0]:
                    await script.add_line_to_result("🟦")

                # blank space should be black
                elif all(znak.isspace() for znak in script.line_processing_list) or \
                        script.line_processing_list == ['']:
                    await script.add_line_to_result("⬛")

                # labels have purple
                elif ":" in script.line_processing_list[-1]:
                    await script.add_line_to_result("🟪")

                # flags have white
                elif "!--" in script.line_processing_list[0]:
                    await script.add_line_to_result("⬜")

                # if nothing matches, then error
                else:
                    await script.add_line_to_result("🟥")
                    await script.error_template(0, "Invalid action | Find all here",
                                                link="https://pastebin.com/6C0ry80E")

                    script.errored = True

            await script.send_result_embed()

        except Exception as e:
            await script.ctx.reply("An error occured while generating the overviev.\n"
                                   "Please report it to <@762016625096261652>, thank you.\n"
                                   f"`{e}`")
    del script


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".v / .i"),
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
                  "KILL {CLASSD} Exploded```\n"
                  "It also supports txt files, for when you reach the character limit!",
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

    elif message.attachments and message.attachments[0].filename.endswith('.txt')\
            and message.content.startswith(".v") or message.content.startswith(".V"):

        attachment = message.attachments[0]
        file = await attachment.read()
        file_content = file.decode('utf-8')
        script = VerifyCode(message, bot, file_content)

        await proccess_verify_request(script)

    elif message.content.startswith(".v") or message.content.startswith(".V"):
        print(f"{message.author} requested code verification")
        script = VerifyCode(message, bot, message.content)

        await proccess_verify_request(script)

    elif message.content == "qwerty" and message.author.id == 762016625096261652:
        role_id = 846021698603319336
        for member in message.guild.members:
            for role in member.roles:
                if role.id == role_id:
                    role = get(message.guild.roles, id=role_id)

                    print(f"{member.name} posiada rolę {role}")

                    await member.send(f"Hi! I see that you have a role `{role.name}` in the {message.guild.name}!")


bot.run(TOKEN)
