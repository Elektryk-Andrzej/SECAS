import discord
from label_visualiser import LabelVisualiser


class IOHandler:
    def __init__(self, msg, bot):
        self.msg: discord.Message = msg
        self.bot: discord.Client = bot
        self.lv: LabelVisualiser = LabelVisualiser.LabelVisualiser()

    async def visualise(self) -> str:
        max_line_len: int = 40

        self.lv.format_script(self.msg.content)
        self.lv.register_labels()
        self.lv.register_matrix()
        self.lv.register_actions()
        self.lv.draw_connections()

        result: str = "```"
        results = self.lv.get_result()
        for index, line in enumerate(results):
            if index == 0:
                continue

            result += (
                f"{line} | {self.lv.script[index]}\n"
                if len(self.lv.script[index]) <= max_line_len else
                f"{line} | {self.lv.script[index][:max_line_len]}...\n"
            )

        return result + "```"

