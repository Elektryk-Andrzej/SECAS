import discord
import discord.ext.commands
from discord.ext import commands

from DO_NOT_SHIP.TOKEN import TOKEN
# from discord.utils import get
from class_CodeVerifier import CodeVerifier
from class_Flowchart import Flowchart

BOT = commands.Bot(command_prefix=".", intents=discord.Intents.all())


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
                    await script.error_template(0, "Invalid action")

                    script.errored = True

            if lines_done == 1:
                await script.no_code()
            else:
                await script.send_result_embed()

        except Exception as e:
            await script.ctx.reply("An error occured while generating the overviev.\n"
                                   "Please report it to <@762016625096261652>, thank you.\n"
                                   f"`{e}`")
            with open("logs.txt", "rb") as file:
                # noinspection PyTypeChecker
                await script.ctx.channel.send("## Debug", file=discord.File(file, "logs.txt"))

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
                discord.SelectOption(label="Contributions", value="contributors"),
                discord.SelectOption(label="Supporting", value="donate"),
            ]
        )
        async def select_error(self, interaction: discord.Interaction,
                               select_item: discord.ui.Select):

            await interaction.response.defer()
            answer = select_item.values

            if answer[0] == "description":
                await self.embed.edit(embed=discord.Embed(title=f"What is {BOT.user.name}?", description=
                "**Scripted Events Code Analysis System** "
                "is a tool made to check if your SE code doesn't contain any errors. "
                "If an error is found, SECAS will specify where and why it is."))

            elif answer[0] == "usage":
                await self.embed.edit(embed=discord.Embed(title=f"How to use {BOT.user.name}?", description=
                    "It's very simple! Just write `.v` and put all of your code below. E.g.\n"
                    "```\n"
                    ".v\n"
                    "SETROLE * ClassD\n"
                    "HINTPLAYER {CLASSD} 6 You have 45 seconds of life left!\n"
                    "WAITSEC 45\n"
                    "KILL {CLASSD} Exploded```\n"
                    "It also supports txt files, for when you reach the discord character limit!\n"
                    "If you upload a .txt file, the rest of the message will be ignored."))

            elif answer[0] == "bugs":
                await self.embed.edit(embed=discord.Embed(
                    title=f"What should I do when I encounter a {BOT.user.name} bug?",
                    description=
                    f"Just ping <@762016625096261652> and explain the bug. \n"
                    f"If you do that enough times, as special thanks you will be granted a place in this embed "
                    f"as a contributor!"))

            elif answer[0] == "contributors":
                await self.embed.edit(embed=discord.Embed(
                    title=f"{BOT.user.name} project contributors!",
                    description=
                    f"### <:elektryk_andrzej:1146409927032709190> <@762016625096261652> - Lead developer\n"
                    f"### <:jraylor:1148181032772849665> <@533344220585394206> - Supporter\n"
                    f"### <:saskyc:1146409898314309643> <@543711481837912078> - Betatester & Supporter\n"))

            elif answer[0] == "donate":
                await self.embed.edit(embed=discord.Embed(
                    title=f"{BOT.user.name} supporters!",
                    description=
                    f"# <:jraylor:1148181032772849665> <@533344220585394206> - 8mo :heart:\n"
                    f"# <:saskyc:1146409898314309643> <@543711481837912078> - 1mo :heart:\n"
                    f"By donating to my [ko-fi](https://ko-fi.com/elektrykandrzej) "
                    f"or directly through PayPal (pieniek.olek@gmail.com), you will recieve access "
                    f"to the newest features of SECAS, and a big thank you <3"))

            else:
                return

        async def send_initial_embed(self):
            self.embed = await self.message.reply(
                embed=discord.Embed(
                    title=f"{BOT.user.display_name} help center"), mention_author=False)

    select_menu = SelectMenu(message)
    await message.channel.send(embed=(await select_menu.send_initial_embed()), view=select_menu)


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

    if message.content.upper().startswith(".I") or BOT.user.mentioned_in(message):
        await info_embed(message)
        return

    elif message.attachments and message.attachments[0].filename.endswith('.txt') \
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

    elif message.content.upper().startswith(".D"):
        print(f"{message.author} requested code verification")
        script = CodeVerifier(message, BOT, message.content)

        await proccess_verify_request(script, False)
        with open("logs.txt", "rb") as file:
            # noinspection PyTypeChecker
            await message.reply("## Debug", file=discord.File(file, "logs.txt"))

    '''elif message.content.upper().startswith(".F"):
        program_file = Flowchart((".v\n"
         "SETROLE {CLASSD} Scp939 2\n"
         "GOTOIF TRUE FALSE {WAVERESPAWNING} = TRUE\n"
         "\n"
         "TRUE:\n"
         "CASSIE SUSSER\n"
         "STOP"
         "\n"
         "FALSE:\n"
         "KILL {CLASSD} 3 DEBIL\n"
         "STOP"))
        program_file = Flowchart(message.content)
        await program_file.analyze()
        product = await program_file.execute()

        await message.channel.send(f"```{product}```")'''

if __name__ == "__main__":
    BOT.run(TOKEN)
    TOKEN = None
