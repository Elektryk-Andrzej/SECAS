import class_DataHandler
import class_ErrorHandler
import discord
from datetime import *


class Utils:
    def __init__(self, data: class_DataHandler.DataHandler):
        self.data = data

    # Get a value from the line list, report error if outside of range
    async def get_str_from_line(self, line_index) -> str:
        try:
            return str(self.data.line_in_list[line_index])

        except IndexError:
            await (class_ErrorHandler.ErrorHandler(self.data).
                   secas_error(line_index,
                               f"Tried to access a value outside of range (`{line_index}`), "
                               f"The last value was granted instead (`{str(self.data.line_in_list[-1])}`). "
                               f"Please report this error to {self.data.andrzej_ping}"))
            return str(self.data.line_in_list[-1])

    @staticmethod
    async def strip_brackets(val: str) -> str:
        return val.replace("{", "").replace("}", "")

    async def log(self, reason):
        with open(self.data.tag, "a") as file:
            date = datetime.now()

            file.write(f"{datetime.strftime(date, r'%H:%M:%S.%f')} - {reason}\n")

            file.close()

    # Format all of the data and add it into a list, from which it will be assembled into an embed
    async def add_line_to_result(self, emoji: str):
        if emoji == "⬛":
            to_append = f"`{len(self.data.processed_lines) + 1}`{emoji}"
            self.data.processed_lines.append(to_append)
            return

        to_append = f"`{len(self.data.processed_lines) + 1}`{emoji}` {self.data.line_in_str} `"
        self.data.processed_lines.append(to_append)

    # Idk why i did this, it doesnt make anything easier
    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)
