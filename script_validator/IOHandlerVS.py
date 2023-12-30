from script_validator import Data, VerdictHandler, ActionHandler, Utils, LogHandler
import discord
import inspect


class IOHandler:
    def __init__(self, data: Data.Data, msg, bot):
        self.data: Data.Data = data
        self.bot = bot
        self.msg = msg
        self.verdict_handler: VerdictHandler.VerdictHandler = data.verdict_handler_object
        self.action_handler: ActionHandler.ActionHandler = data.action_handler_object
        self.utils: Utils.Utils = data.utils_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

    async def format_code(self, count_first_line: bool) -> list:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            count_first_line=count_first_line
        )

        self.data.code = [str(line.strip()).split(" ") for line in self.data.code.splitlines()]

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

    async def proccess_request(self) -> None:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe())
        )

        count_first_line: bool
        if self.msg.attachments and self.msg.attachments[0].filename.endswith('.txt'):
            attachment = self.msg.attachments[0]
            message_content = await attachment.read()
            self.data.code = message_content.decode("utf-8")
            count_first_line = True
        else:
            self.data.code = self.msg.content
            count_first_line = False

        await self.format_code(count_first_line=count_first_line)

        await self.get_labels()

        line: list
        for index, line in enumerate(self.data.code):
            index: int
            line: list

            await self.logs.log(f"Checking line {index+1} with value {line}")

            self.data.code_index += 1
            self.data.line = line
            self.data.line_verdict_set = False
            self.data.line_to_copy_for_verdict_processing = line

            if (action_name := line[0]) in self.action_handler.actions:
                action_done = await self.action_handler.actions[action_name]()

                if action_done:
                    await self.verdict_handler.line_verdict(self.data.LineVerdict.PASSED)

                else:
                    if not self.data.line_verdict_set:
                        await self.verdict_handler.line_verdict(
                            self.data.LineVerdict.NOT_CHECKABLE,
                            " ".join(self.data.line),
                            "SECAS ERROR; report to dev"
                        )

            elif "#" in line[0]:
                await self.verdict_handler.line_verdict(self.data.LineVerdict.COMMENT)

            elif ":" in line[-1] and len(line) == 1:
                await self.verdict_handler.line_verdict(self.data.LineVerdict.LABEL)

            elif "!--" in line[0] and len(self.data.line) == 2:
                await self.verdict_handler.line_verdict(self.data.LineVerdict.FLAG)

            elif line == ['']:
                await self.verdict_handler.line_verdict(self.data.LineVerdict.EMPTY)

            else:
                closest_match = await self.utils.get_closest_match(
                    action_name, tuple(self.action_handler.actions.keys())
                )
                await self.verdict_handler.error_template(0, "Invalid action", closest_match)

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

    async def get_overview_embed_color(self) -> int:
        for element in self.data.processed_lines:
            if element[0] == "🟥":
                return 0xdd2e44
        else:
            return 0xfdcb58

    async def format_processed_lines_to_overview(self) -> list:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()))
        character_limit: int = 2000
        overview_lines: list = []

        for element in self.data.processed_lines:
            color, normal_line, _, _, index, _, _, _ = element

            if color != "⬛":
                overview_lines.append(f"`{index}`{color} `{normal_line}`\n")
            else:
                overview_lines.append(f"`{index}`{color}\n")

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
        character_limit: int = 2000
        error_summary_lines: list = []

        for element in self.data.processed_lines:
            color, _, line_to_print, reason, index, closest_match, closest_match_print_string, footer = element

            if not reason or not line_to_print:
                continue

            new_line_prefix = "\nㅤ\n" if len(error_summary_lines) != 0 else ""

            if closest_match is not None:
                error_summary_lines.append(
                    f"{new_line_prefix}"
                    f"## > {reason}\n"
                    f"`{index}`{color} `{line_to_print}`\n"
                    f"### {closest_match_print_string[0]}`{closest_match}`{closest_match_print_string[1]}"
                )

            elif footer is not None:
                error_summary_lines.append(
                    f"{new_line_prefix}"
                    f"## > {reason}\n"
                    f"`{index}`{color} `{line_to_print}`\n"
                    f"### {footer}"
                )

            else:
                error_summary_lines.append(
                    f"{new_line_prefix}"
                    f"## > {reason}\n"
                    f"`{index}`{color} `{line_to_print}`"
                )

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
        color_overview = await self.get_overview_embed_color()
        color_no_error = 0x77b255

        if self.data.show_overview:
            for embed_content_list in await self.format_processed_lines_to_overview():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(
                    embed=discord.Embed(
                        description=embed_content,
                        color=color_overview
                    )
                )

            for embed_content_list in await self.format_processed_lines_to_error_summary():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(embed=discord.Embed(
                        description=embed_content,
                        color=color_overview
                    )
                )

        else:
            for embed_content_list in await self.format_processed_lines_to_overview():
                embed_content = "".join(embed_content_list)

                await self.msg.channel.send(embed=discord.Embed(
                        description=embed_content,
                        color=color_no_error
                    )
                )

        await self.logs.close(None)
        return
