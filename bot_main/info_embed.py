import discord


class Descriptions:
    description: str = (
        "**Scripted Events Code Analysis System** "
        "is a multi-purpose tool for any SEL developer looking to debug their code.\n"
        "It's simple design and ease of use makes it perfect for anyone!"
    )

    verify_script_usage: str = (
        "It's very simple! Just write `.vs` and put all of your code below."
        "It also supports txt files, for when you reach the discord character limit!"
    )



class SelectMenu(discord.ui.View):
    def __init__(self, message, bot):
        super().__init__()
        self.message: discord.Message = message
        self.embed = None
        self.bot: discord.Client = bot
        self.desc: Descriptions = Descriptions()

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

        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        answer = select_item.values

        if answer[0] == "description":
            await self.embed.edit(embed=discord.Embed(
                title=f"What is {self.bot.user.name}?",
                description=self.desc.description
            ))

        elif answer[0] == "usage":
            await self.embed.edit(embed=discord.Embed(
                title=f"How to verify my script?",
                description=self.desc.verify_script_usage
            ))

        elif answer[0] == "bugs":
            await self.embed.edit(embed=discord.Embed(
                title=f"What should I do when I encounter a {self.bot.user.name} bug?",
                description=f"Just ping <@762016625096261652>, explain the bug and give a copy of the script that "
                            f"has caused the problem."))

        elif answer[0] == "donate":
            await self.embed.edit(embed=discord.Embed(
                title=f"{self.bot.user.name} supporters!",
                description=f"# <:saskyc:1146409898314309643> <@543711481837912078> - 1mo\n"
                            f"# <:jraylor:1148181032772849665> <@533344220585394206> - 8mo\n"
                            f"# <:xxnubnubxx:1156643754552336504> <@389059604895498243> - 2mo\n"
                            f"Want to support the SECAS project? Consider donating!\n"
                            f"## > [ko-fi](https://ko-fi.com/elektrykandrzej)\n"))

        else:
            return

    async def send_initial_embed(self):
        self.embed = await self.message.reply(
            embed=discord.Embed(
                title=f"About {self.bot.user.display_name}"), mention_author=False)
        return self.embed


async def info_embed(message: discord.Message, bot: discord.Client):
    select_menu = SelectMenu(message, bot)
    embed = await select_menu.send_initial_embed()

    await message.channel.send(
        view=select_menu
    )
