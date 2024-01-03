import discord


class Descriptions:
    description: str = (
        "**Scripted Events Code Analysis System** "
        "is a multi-purpose tool for any SEL developer. "
        "SECAS is helpful with debugging, working with labels or browisng the shelp! "
        "It's simple design and ease of use makes it enjoyable to use."
    )

    verify_script_usage: str = (
        "SECAS supports `3 commands`, those being:\n"
        "- `.vs` (verify script) - Checks for syntax errors.\n"
        "- `.vl` (visualise labes) - Shows redirect logic.\n"
        "- `.sh` (script help) - Brings up a summary of an action."
    )


class SelectMenu(discord.ui.View):
    def __init__(self, message, bot):
        super().__init__()
        self.message: discord.Message = message
        self.embed = None
        self.bot: discord.Client = bot
        self.desc: Descriptions = Descriptions()

    @discord.ui.select(
        placeholder="Select an option",
        options=[
            discord.SelectOption(label="What is SECAS?", value="description"),
            discord.SelectOption(label="Command - Verify Script", value="vs usage"),
            discord.SelectOption(label="Supporting!", value="donate"),
        ]
    )
    async def select_error(self, interaction: discord.Interaction,
                           select_item: discord.ui.Select):

        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        answer = select_item.values

        if answer[0] == "description":
            await self.embed.edit(
                embed=discord.Embed(
                    title="What is SECAS?",
                    description=self.desc.description,
                    color=0xeddb9f
                )
            )

        elif answer[0] == "vs usage":
            await self.embed.edit(
                embed=discord.Embed(
                    title="Which commands can I use?",
                    description=self.desc.verify_script_usage,
                    color=0xeddb9f
                )
            )

        elif answer[0] == "donate":
            await self.embed.edit(
                embed=discord.Embed(
                    title=f"{self.bot.user.name} supporters!",
                    description=
                    f"# <:saskyc:1146409898314309643> <@543711481837912078> - 1mo\n"
                    f"# <:jraylor:1148181032772849665> <@533344220585394206> - 8mo\n"
                    f"# <:xxnubnubxx:1156643754552336504> <@389059604895498243> - 2mo\n"
                    f"Enjoying the SECAS project? Consider supporting!\n"
                    f"## > [ko-fi](https://ko-fi.com/elektrykandrzej)\n",
                    color=0xeddb9f
                )
            )

        else:
            return

    async def send_initial_embed(self):
        self.embed = await self.message.reply(
            embed=discord.Embed(
                title=f"About {self.bot.user.display_name}", color=0xeddb9f), mention_author=False)
        return self.embed


async def info_embed(message: discord.Message, bot: discord.Client):
    select_menu = SelectMenu(message, bot)
    await select_menu.send_initial_embed()

    await message.channel.send(
        view=select_menu
    )
