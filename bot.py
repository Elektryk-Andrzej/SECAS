import asyncio
import discord
from discord.ext import commands
import os
import IOHandler
from TOKEN import TOKEN
import DataHandler

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def info_embed(message):
    # noinspection PyUnresolvedReferences
    class SelectMenu(discord.ui.View):
        def __init__(self, message):
            super().__init__()
            self.message = message
            self.embed = None

        @discord.ui.select(
            placeholder="Select option",
            options=[
                discord.SelectOption(label="What is SECAS?", value="description"),
                discord.SelectOption(label="How to use SECAS?", value="usage"),
                discord.SelectOption(label="Bug reporting", value="bugs"),
                discord.SelectOption(label="Supporting", value="donate"),
            ]
        )
        async def select_error(self, interaction: discord.Interaction,
                               select_item: discord.ui.Select):

            await interaction.response.defer()
            answer = select_item.values

            if answer[0] == "description":
                await self.embed.edit(embed=discord.Embed(
                    title=f"What is {bot.user.name}?",
                    description="**Scripted Events Code Analysis System** "
                                "is a tool made to check if your SE code doesn't contain any errors. "
                                "If an error is found, SECAS will specify where and why it is.\n"
                                "This bot will never collect any data about you and your scripts."
                ))

            elif answer[0] == "usage":
                await self.embed.edit(embed=discord.Embed(
                    title=f"How to use {bot.user.name}?",
                    description="It's very simple! Just write `.v` and put all of your code below. E.g.\n"
                                "```\n"
                                ".v\n"
                                "SETROLE * ClassD\n"
                                "HINTPLAYER {CLASSD} 6 You have 45 seconds of life left!\n"
                                "WAITSEC 45\n"
                                "KILL {CLASSD} Exploded```\n"
                                "It also supports txt files, for when you reach the discord character limit!\n"
                                "If you upload a .txt file, the rest of the message will be ignored."
                ))

            elif answer[0] == "bugs":
                await self.embed.edit(embed=discord.Embed(
                    title=f"What should I do when I encounter a {bot.user.name} bug?",
                    description=f"Just ping <@762016625096261652>, explain the bug and give a copy of the script that "
                                f"has caused the problem."))

            elif answer[0] == "donate":
                await self.embed.edit(embed=discord.Embed(
                    title=f"{bot.user.name} supporters!",
                    description=f"# <:saskyc:1146409898314309643> <@543711481837912078> - 1mo\n"
                                f"# <:jraylor:1148181032772849665> <@533344220585394206> - 8mo\n"
                                f"# <:xxnubnubxx:1156643754552336504> <@389059604895498243> - 2mo\n"
                                f"Want to support the SECAS project? Consider donating!\n"
                                f"> [ko-fi](https://ko-fi.com/elektrykandrzej)\n"
                                f"> "))

            else:
                return

        async def send_initial_embed(self):
            self.embed = await self.message.reply(
                embed=discord.Embed(
                    title=f"About {bot.user.display_name}"), mention_author=False)

    select_menu = SelectMenu(message)
    await message.channel.send(embed=(await select_menu.send_initial_embed()), view=select_menu)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".v / .i"),
        status=discord.Status.online)


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.content.upper().startswith(".I") or str(bot.user.id) in message.content:
        await info_embed(message)
        return

    elif message.content.upper().startswith(".V"):
        data = DataHandler.Data()
        io_handler = IOHandler.IOHandler(data, message, bot)

        if os.path.exists(f"LOGS/{data.log_file_name}") or os.path.exists(f"LOGS\\{data.log_file_name}"):
            await asyncio.sleep(1.5)
            data = DataHandler.Data()

        count_first_line: bool
        if message.attachments and message.attachments[0].filename.endswith('.txt'):
            attachment = message.attachments[0]
            message_content = await attachment.read()
            data.code = message_content.decode("utf-8")
            count_first_line = True
        else:
            data.code = message.content
            count_first_line = False

        await io_handler.proccess_verify_request(count_first_line=count_first_line)

    elif message.content.upper().startswith(".H"):
        embed = \
            discord.Embed(title=f"About getting help from others",
                          description="""
                          1. If you want someone to help you (which is the thing you're doing), 
                          you want your question to be as easy to understand as possible.
                          No one is going to try and decipher what you are asking for.
                              
                          2. It's in your best intrest to respect people helping you, because
                          they're doing it for free, and they can and will refuse to help you if
                          you don't treat them like human beings.
                              
                          3. Ask about certian things __AFTER__ reading the documentation
                          and trying something out for yourself. This way you'll learn to not
                          be reliant on other people only.
                          
                          """)
        embed.add_field(name="1:",
                        value="If you want someone to help you (which is the thing you're doing), "
                              "you want your question to be as easy to understand as possible.\n"
                              "No one is going to try and decipher what you are asking for.")

        await message.reply(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)
    TOKEN = None
