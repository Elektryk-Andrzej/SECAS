import shelp.shelp_info
import discord
import script_validator.Utils


class IOHandler:
    def __init__(self, msg: discord.Message):
        self.msg = msg
        self.actions = {
            var_name: var_value for
            var_name, var_value in
            shelp.shelp_info.__dict__.items()
            if not var_name.startswith('__')
        }

        self.closest_match = script_validator.Utils.Utils.get_closest_match

    async def get_action_info(self, action: str):
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

        await self.msg.reply(embed=embed_to_send)


