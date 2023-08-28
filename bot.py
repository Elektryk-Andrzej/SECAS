import discord
import discord.ext.commands
from discord.ext import commands

from DO_NOT_SHIP.TOKEN import TOKEN
from discord.utils import get
from class_CodeVerifier import CodeVerifier

BOT = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def proccess_verify_request(script, count_first_line: bool):
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
                if index == 0 and not count_first_line:
                    continue

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

                # comments have blue
                elif "#" in script.line_processing_list[0]:
                    await script.add_line_to_result("🟦")

                # blank spaces have black
                elif all(znak.isspace() for znak in script.line_processing_list) or \
                        script.line_processing_list == ['']:
                    await script.add_line_to_result("⬛")

                # labels have purple
                elif ":" in script.line_processing_list[-1] and len(script.line_processing_list) == 1:
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


@BOT.event
async def on_ready():
    print(f"Zalogowano jako {BOT.user}")
    await BOT.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".v / .i"),
        status=discord.Status.online)


@BOT.event
async def on_message(message):
    if message.author.id == BOT.user.id:
        return

    if message.content.startswith(".i") or message.content.startswith(".I"):
        print(f"{message.author} requested info")
        embed = discord.Embed(title=None,
                              description=None,
                              color=0xe84d97)

        embed.add_field(
            name=f"What is {BOT.user.name}?",
            value="**Scripted Events Code Analysis System** "
                  "is a tool made to check if your SE code doesn't contain any errors."
                  "If an error is found, SECAS will specify where and why it is.",
            inline=False
        )
        embed.add_field(
            name=f"How to use {BOT.user.name}?",
            value="It's very simple! Just write `.v` and put all of your code below. E.g.\n"
                  "```\n"
                  ".v\n"
                  "SETROLE * ClassD\n"
                  "HINTPLAYER {CLASSD} 6 You have 45 seconds of life left!\n"
                  "WAITSEC 45\n"
                  "KILL {CLASSD} Exploded```\n"
                  "It also supports txt files, for when you reach the discord character limit!",
            inline=False
        )

        embed.add_field(
            name=f"What should I do when I encounter a {BOT.user.name} bug?",
            value=f"Just ping <@762016625096261652> and explain the bug. \n"
                  f"If you do that enough times, as special thanks you will be granted a place in this embed "
                  f"as a contributor!",
            inline=False
        )

        embed.add_field(
            name=f"{BOT.user.name} project contributors!",
            value=f"`elektryk_andrzej` - Lead developer\n"
                  f"`saskyc` - Betatester",
            inline=False
        )
        await message.reply(embed=embed, mention_author=False)
        return

    elif message.attachments and message.attachments[0].filename.endswith('.txt')\
            and message.content.upper().startswith(".V"):

        attachment = message.attachments[0]
        file = await attachment.read()
        file_content = file.decode('utf-8')
        script = CodeVerifier(message, BOT, file_content)

        await proccess_verify_request(script, True)

    elif message.content.upper().startswith(".V"):
        print(f"{message.author} requested code verification")
        script = CodeVerifier(message, BOT, message.content)

        await proccess_verify_request(script, False)

if __name__ == "__main__":
    BOT.run(TOKEN)
