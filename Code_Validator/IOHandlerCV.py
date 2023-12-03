from Code_Validator import Data, VerdictHandler, ActionHandler, Utils, LogHandler
from datetime import *
import discord
import inspect
import os


class IOHandler:
    def __init__(self, data: Data.Data, msg, bot):
        self.data: Data.Data = data
        self.bot = bot
        self.msg = msg
        self.verdict_handler: VerdictHandler.VerdictHandler = data.verdict_handler_object
        self.action_handler: ActionHandler.ActionHandler = data.action_handler_object
        print("action handler required")
        self.utils: Utils.Utils = data.utils_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

        date = datetime.now()
        self.data.log_file_name = (f"../Logs/{datetime.strftime(date, '%d;%m %H-%M-%S')} "
                                   f"@ {msg.author.display_name}")

        if not os.path.exists("../Logs"):
            os.makedirs("../Logs")
            
        with open(self.data.log_file_name, "x") as file:
            file.close()

    async def format_code(self, count_first_line: bool) -> list:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))

        lines = self.data.code.splitlines()

        self.data.code = [line for line in lines]

        self.data.code = [line.split(" ") for line in lines]

        if not count_first_line:
            self.data.code.pop(0)

        await self.logs.close(self.data.code)

        return self.data.code

    async def get_labels(self) -> None:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))

        for index, line in enumerate(self.data.code):
            if len(line) == 1 and str(line[0]).endswith(":"):
                label = str(line[0]).strip(":")
                self.data.labels.append(label)

                await self.logs.log(f"Registered a new label: \"{label}\"")

        await self.logs.close(None)

    async def proccess_verify_request(self, count_first_line: bool) -> None:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            count_first_line=count_first_line
        )

        async with self.msg.channel.typing():
            await self.format_code(count_first_line=count_first_line)

            await self.get_labels()

            line: list
            for index, line in enumerate(self.data.code):
                await self.logs.log(f"Checking line {index+1} with value {line}")

                self.data.code_index += 1
                self.data.line = line
                self.data.line_verdict_set = False

                if (action_name := line[0]) in self.action_handler.actions:
                    action_done = await self.action_handler.actions[action_name]()

                    if action_done:
                        await self.verdict_handler.line_verdict(self.data.LineVerdictType.PASSED)

                    else:
                        if not self.data.line_verdict_set:
                            await self.verdict_handler.line_verdict(
                                self.data.LineVerdictType.ERRORED,
                                " ".join(self.data.line),
                                "No reason specifed, consider this a SECAS error"
                            )

                elif "#" in line[0]:
                    await self.verdict_handler.line_verdict(self.data.LineVerdictType.COMMENT)

                elif ":" in line[-1] and len(line) == 1:
                    await self.verdict_handler.line_verdict(self.data.LineVerdictType.LABEL)

                elif "!--" in line[0] and len(self.data.line) == 2:
                    await self.verdict_handler.line_verdict(self.data.LineVerdictType.FLAG)

                elif line == ['']:
                    await self.verdict_handler.line_verdict(self.data.LineVerdictType.EMPTY)

                else:
                    await self.verdict_handler.error_template(0, "Invalid action")

            if self.data.code_index == 0:
                await self.msg.reply("No code found! First line is always ignored.")
            else:
                await self.send_result_embed()

            '''except Exception as e:
                await self.ctx.reply("An error occured while generating the overviev.\n"
                                     f"Please report it to {self.data.andrzej_ping}, thank you.\n"
                                     f"`{e}`",
                                     mention_author=False)'''

        await self.logs.close(None)

    async def format_processed_lines_to_overview(self) -> list:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))

        character_limit = 2000

        overview_lines = []
        for element in self.data.processed_lines:
            if not element[0] == "⬛":
                overview_lines.append(f"`{element[4]}`{element[0]} `{element[1]}`\n")
            else:
                overview_lines.append(f"`{element[4]}`{element[0]}\n")

        devided_overview_lines = []
        current_list = []

        for element in overview_lines:
            if sum(map(len, current_list)) + len(str(element)) <= character_limit:
                current_list.append(element)

            else:
                devided_overview_lines.append(current_list)
                current_list = [element]

        if current_list:
            devided_overview_lines.append(current_list)

        await self.logs.close(devided_overview_lines)
        return devided_overview_lines

    async def format_processed_lines_to_error_summary(self) -> list:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))

        character_limit = 2000

        error_summary_lines = []
        for element in self.data.processed_lines:
            if not element[3] or not element[2]:
                continue

            error_summary_lines.append(f"### > {element[3]}\n`{element[4]}`{element[0]} `{element[2]}`\n")

        devided_error_summary_lines = []
        current_list = []

        for element in error_summary_lines:
            if sum(map(len, current_list)) + len(str(element)) <= character_limit:
                current_list.append(element)

            else:
                devided_error_summary_lines.append(current_list)
                current_list = [element]

        if current_list:
            devided_error_summary_lines.append(current_list)

        await self.logs.close(devided_error_summary_lines)
        return devided_error_summary_lines

    async def send_result_embed(self) -> None:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))
        color_error = 0xdd2e44
        color_no_error = 0x77b255

        if self.data.errored:
            for embed_content_list in await self.format_processed_lines_to_overview():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(
                    embed=discord.Embed(
                        title=None,
                        description=embed_content,
                        color=color_error
                    )
                )

            for embed_content_list in await self.format_processed_lines_to_error_summary():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(embed=discord.Embed(
                        title=None,
                        description=embed_content,
                        color=color_error
                    )
                )

        else:
            for embed_content_list in await self.format_processed_lines_to_overview():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(embed=discord.Embed(
                        title=None,
                        description=embed_content,
                        color=color_no_error
                    )
                )

        await self.logs.close(None)
        return
