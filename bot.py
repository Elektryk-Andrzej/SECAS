import discord
import discord.ext.commands
from discord.ext import commands
from DO_NOT_SHIP.TOKEN import TOKEN
from class_CodeVerifier import CodeVerifier

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


async def delete_empty_params(line_processing_list: list) -> None:
    index_to_pop = []

    for index, value in enumerate(line_processing_list):
        if value == "" or value == " ":
            index_to_pop.append(index)

    for i in range(len(index_to_pop) - 1, -1, -1):
        line_processing_list.remove(index_to_pop[i])


async def proccess_verify_request(script, count_first_line: bool):
    async with (script.ctx.channel.typing()):
        lines_done = 0
        try:
            # register all labels
            for index, line in enumerate(script.code):
                script.line_processing_list = line.split(" ")
                script.line_processing_list[-1].strip("\n")

                if index == 0 and len(script.line_processing_list) > 1 and \
                        script.line_processing_list[0].startswith("."):
                    script.line_processing_list.pop(0)

                if ":" in (label := script.line_processing_list[-1]):
                    script.labels.append(label.strip(":"))

            # for all lines to be verified
            for index, line in enumerate(script.code):
                lines_done += 1

                # delete .v from the first line
                if index == 0 and not count_first_line:
                    continue

                script.line_processing_index = index
                script.line_processing_str = line.strip("\n")
                script.line_processing_list = line.split(" ")
                script.line_processing_list[-1].strip("\n")
                script.line_already_added_to_result = False
                await delete_empty_params(script.line_processing_list)

                # run check for action if exists
                try:
                    action_done = await script.actions[script.line_processing_list[0]]()

                    if action_done:
                        await script.add_line_to_result("🟩")
                    else:
                        await script.add_line_to_result("🟥")
                        script.errored = True

                    continue
                except:
                    pass

                # comments have blue
                if "#" in script.line_processing_list[0]:
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
                    await script.error_template(0, "Invalid action")

                    script.errored = True

            if lines_done == 1:
                await script.error_no_code()
            else:
                await script.send_result_embed()

        except Exception as e:
            await script.ctx.reply("An error occured while generating the overviev.\n"
                                   "Please report it to <@762016625096261652>, thank you.\n"
                                   f"`{e}`",
                                   mention_author=False)

    script.custom_variables = []


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
    print(f"Zalogowano jako {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f".v / .i"),
        status=discord.Status.online)


# noinspection PyTypeChecker
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.content.upper().startswith(".I") or bot.user.mentioned_in(message):
        await info_embed(message)
        return

    elif message.attachments and message.attachments[0].filename.endswith('.txt') \
            and message.content.upper().startswith(".V"):

        attachment = message.attachments[0]
        file = await attachment.read()
        file_content = file.decode('utf-8')
        script = CodeVerifier(message, bot, file_content)

        await proccess_verify_request(script, True)

    elif message.content.upper().startswith(".V"):
        print(f"{message.author} requested code verification")
        script: CodeVerifier = CodeVerifier(message, bot, message.content)

        await proccess_verify_request(script, False)

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
