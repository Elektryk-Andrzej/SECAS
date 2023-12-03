import discord
from Label_Visualiser import LabelVisualiser


class IOHandler:
    def __init__(self, msg, bot):
        self.msg: discord.Message = msg
        self.bot: discord.Client = bot
        self.lv: LabelVisualiser = LabelVisualiser.LabelVisualiser()

    async def visualise(self) -> str:
        self.lv.format_script(self.msg.content)
        self.lv.register_labels()
        self.lv.set_matrix()
        self.lv.register_redirect_actions()

        result: str = "```"
        for index, line in enumerate(self.lv.get_result()):
            if index == 0:
                continue

            result += f"{line} | {self.lv.script[index]}\n"

        return result + "```"

