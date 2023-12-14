import shelp.action_info
import discord
import script_validator.Utils


class IOHandler:
    def __init__(self, msg: discord.Message):
        self.msg = msg
        self.actions = {
            var_name: var_value for
            var_name, var_value in
            shelp.action_info.__dict__.items()
            if not var_name.startswith('__')
        }
        self.action_check_keyword: tuple = "ACT", "ACTION", "A"
        self.variable_check_keyword: tuple = "VAR", "VARIABLE", "V"

        self.closest_match = script_validator.Utils.Utils.get_closest_match

    async def process_help_request(self):
        message: list = self.msg.content.strip().upper().split(" ")

        if len(message) < 2:
            await self.msg.reply(
                "Mode not specified!\n"
                "Available modes:\n"
                f"- Action mode - {self.action_check_keyword}\n"
                f"- Variable mode - {self.variable_check_keyword}",
                mention_author=False
            )
            return

        if len(message) < 3:
            await self.msg.reply(
                "Please specify an action/variable!\n"
                "You can use ` * ` to get a list of all available actions/variables.",
                mention_author=False
            )
            return

        if message[1] in self.variable_check_keyword:
            pass

        elif message[1] in self.action_check_keyword:
            await self.get_action_info("".join(message[2:]))

        else:
            await self.msg.reply(
                "Wrong mode specified!\n"
                "Available modes:\n"
                f"- Action mode - {self.action_check_keyword}\n"
                f"- Variable mode - {self.variable_check_keyword}",
                mention_author=False
            )

    async def get_action_info(self, action: str):
        action = action.upper().strip()
        message_to_send: str = ""

        if action == "*":
            await self.get_all_action_info()
            return

        if action not in self.actions.keys():
            message_to_send = f"Found no results for \"{action}\", showing definition for most similar action."
            action = await self.closest_match(action, tuple(self.actions.keys()))

        action_params: list = self.actions[action]
        embed_to_send: discord.Embed = discord.Embed(title=action_params[0], description=action_params[1])

        for param in action_params[2]:
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

        await self.msg.reply(message_to_send, embed=embed_to_send, mention_author=False)

    async def get_all_action_info(self):
        embed_to_send: discord.Embed = discord.Embed(title="Action list", description="", color=0xeddb9f)
        for index, action in enumerate(self.actions.items()):
            print(action)
            embed_to_send.add_field(
                name=action[0],
                value=action[1][1] if action[1][1] is not None else "", inline=False)

            if index % 30 == 0 and index != 0:
                await self.msg.channel.send(embed=embed_to_send)
                embed_to_send: discord.Embed = discord.Embed(title="", description="", color=0xeddb9f)

        await self.msg.channel.send(embed=embed_to_send)