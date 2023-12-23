import shelp.action_info
import shelp.variable_info
import discord
import script_validator.Utils
import command_prefixes as cmd


class IOHandler:
    def __init__(self, msg: discord.Message):
        self.msg = msg
        self.actions = {
            var_name: var_value for
            var_name, var_value in
            shelp.action_info.__dict__.items()
            if not var_name.startswith('__')
        }
        self.variables = {
            var_name: var_value for
            var_name, var_value in
            shelp.variable_info.__dict__.items()
            if not var_name.startswith('__')
        }
        self.action_check_keyword: tuple = "ACT", "ACTION", "A"
        self.variable_check_keyword: tuple = "VAR", "VARIABLE", "V"

        self.closest_match = script_validator.Utils.Utils.get_closest_match

    async def process_help_request(self) -> None:
        message: list = self.msg.content.strip().upper().split(" ")
        message = [message[0], "".join(message[1:])]

        if len(message) < 2:
            await self.msg.reply(
                content=(
                    f"## Tutorial on {cmd.visualise_labels}\n"
                    f"`.{cmd.visualise_labels} ACTION NAME` to get info about a specified action."
                    f"`.{cmd.visualise_labels} {{VARIABLE NAME}}` to get info about a specfied variable."
                    f"`.{cmd.visualise_labels} LIST` to get a lis of all actions."
                    f"`.{cmd.visualise_labels} LISTVAR` to get a list of all variables."
                ),
                mention_author=False
            )
            return

        if (key := message[1][1:-1]) in self.variables.keys() and message[1][0] == "{" and message[1][-1] == "}":
            await self.get_info(key, self.variables)

        elif (key := message[1]) in self.actions.keys():
            await self.get_info(key, self.actions)

        elif message[1] == "LIST":
            await self.get_all_info(self.actions)

        elif message[1] == "LISTVAR":
            await self.get_all_info(self.variables)

        else:
            closest_match = await script_validator.Utils.Utils.get_closest_match(
                value=message[1],
                possible_values=(
                    tuple(self.actions.keys()) +
                    tuple([f"{{{var}}}" for var in self.variables.keys()]) +
                    ("LIST", "LISTVAR")
                )
            )

            await self.msg.reply(
                "I couldn't find what you were looking for :(\n"
                f"## Did you mean `{closest_match}`?",
                mention_author=False
            )

    async def get_info(self, key: str, group: dict):
        params: list = group[key]
        embed_to_send: discord.Embed = discord.Embed(title=params[0], description=params[1])

        for param in params[2]:
            param: list
            param_name: str = param[0]
            param_type: str = param[1]
            param_required: str = param[2]
            param_description: str = param[3]

            embed_to_send.add_field(
                name=param_name,
                value=(
                    f"{param_description}\n\n"
                    f"type - `{param_type}`\n"
                    f"required - `{param_required}`"
                ),
                inline=False
            )

        await self.msg.reply(embed=embed_to_send, mention_author=False)

    async def get_all_info(self, group: dict):
        embed_to_send: discord.Embed = discord.Embed(
            title=f"LIST - ALL ACTIONS" if group is self.actions else "LISTVAR - ALL VARIABLES",
            description="",
            color=0xeddb9f
        )
        for index, key in enumerate(group.items()):
            embed_to_send.add_field(
                name=key[1][0],
                value=key[1][1] if key[1][1] is not None else "", inline=False)

            if index % 20 == 0 and index != 0:
                await self.msg.channel.send(embed=embed_to_send)
                embed_to_send: discord.Embed = discord.Embed(title="", description="", color=0xeddb9f)

        await self.msg.channel.send(embed=embed_to_send)