from datetime import *
import discord
import DataHandler
import ActionHandler
import VerdictHandler
import Utils
import inspect
import os


class IOHandler:
    def __init__(self, data: DataHandler.Data, ctx, bot):
        self.data: DataHandler.Data = data
        self.bot = bot
        self.ctx = ctx
        self.error_handler: ErrorHandler.VerdictHandler = ErrorHandler.VerdictHandler(data)
        self.action_handler: ActionHandler.ActionHandler = ActionHandler.ActionHandler(data)
        self.utils: Utils.Utils = Utils.Utils(data)

        date = datetime.now()
        self.data.log_file_name = (f"logs/{datetime.strftime(date, '%d;%m %H-%M-%S')} "
                                   f"@ {ctx.author.display_name}")

        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        with open(self.data.log_file_name, "x") as file:
            file.close()

    async def format_code(self, count_first_line: bool) -> None:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()))
        await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                             f"Will be formatting: {self.data.code}")

        new_code = self.data.code.split("\n")

        for index, line in enumerate(self.data.code):
            if index == 0 and not count_first_line:
                continue

            if "\n" in line:
                line.replace("\n", "")

            new_code.append(line.split(" "))

        self.data.code = new_code

        await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                             f"Formatted to: {self.data.code}")
        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                        None)

    async def get_labels(self) -> None:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()))

        for index, line in enumerate(self.data.code):
            if len(line) == 1 and (label := str(line[0]).endswith(":")):

                self.data.labels.append(label)

                await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                                     f"Registered a new label: {label}")

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                        None)

    async def proccess_verify_request(self, count_first_line: bool) -> None:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                count_first_line=count_first_line)

        async with self.ctx.channel.typing():
            lines_done = 0

            await self.format_code(count_first_line=count_first_line)

            await self.get_labels()

            line: list
            for line in self.data.code:
                lines_done += 1

                if len(line) == 0:
                    await self.utils.line_verdict("⬛")
                    continue

                if (action_name := line[0]) in self.action_handler.actions:
                    action_done = await self.action_handler.actions[action_name]()

                    if action_done:
                        await self.utils.line_verdict("🟩")

                    else:
                        await self.utils.line_verdict("🟥")
                        self.data.errored = True
                        # self.data.lines_errored.append(self.data.current_code_index)

                elif "#" in line[0]:
                    await self.utils.line_verdict("🟦")

                elif ":" in self.data.list_line[-1] and len(self.data.list_line) == 1:
                    await self.utils.line_verdict("🟪")

                elif "!--" in self.data.list_line[0]:
                    await self.utils.line_verdict("⬜")

                else:
                    await self.error_handler.error_template(0, "Invalid action")

            if lines_done == 1:
                await self.ctx.reply("No code found! First line is always ignored.")
            else:
                await self.send_result_embed()

            '''except Exception as e:
                await self.ctx.reply("An error occured while generating the overviev.\n"
                                     f"Please report it to {self.data.andrzej_ping}, thank you.\n"
                                     f"`{e}`",
                                     mention_author=False)'''

        self.data.custom_variables.clear()

    async def send_result_embed(self):
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()))
        character_limit = 2000
        color_error = 0xdd2e44
        color_no_error = 0x77b255
        embed_content = ""

        if self.data.errored:
            await self.ctx.reply(embed=await self.utils.create_embed(
                                             f"Errors found: `{len(self.data.error_reasons)}`",
                                             "",
                                             color_error),
                                 mention_author=False)

            for line in self.data.processed_lines:
                embed_content += f"{line}\n"

                if not len(embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.utils.create_embed(
                                            None,
                                            embed_content,
                                            color_error))
                embed_content = ""

            await self.ctx.channel.send(embed=await self.utils.create_embed(
                                        None,
                                        embed_content,
                                        color_error))
            embed_content = ""

            for line in self.data.error_reasons:
                embed_content += f"### > {line[2]}\n`{line[0]}`🟥` {line[1]} `\n"

                if not len(embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.utils.create_embed(
                                            None,
                                            embed_content,
                                            color_error))

                self.data.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=embed_content,
                                        color=color_error)

        else:
            await self.ctx.reply(embed=await self.utils.create_embed(
                                 "No errors found!",
                                 "",
                                 color_no_error),
                                 mention_author=False)

            for line in self.data.processed_lines:
                embed_content += f"{line}\n"

                if not len(embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.utils.create_embed(
                                            None,
                                            embed_content,
                                            color_no_error))
                self.data.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=embed_content,
                                        color=color_no_error)

        final_embed.set_footer(text=f"{self.bot.user.name}by @elektryk_andrzej",
                               icon_url=self.bot.user.avatar)

        await self.ctx.channel.send(embed=final_embed)
