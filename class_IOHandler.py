from datetime import *
import discord
import class_DataHandler
import class_ActionHandler
import class_ErrorHandler
import class_Utils
import inspect
import os


class IOHandler:
    def __init__(self, data: class_DataHandler.DataHandler, ctx, bot):
        self.data: class_DataHandler.DataHandler = data
        self.bot = bot
        self.ctx = ctx
        self.error_handler: class_ErrorHandler.ErrorHandler = class_ErrorHandler.ErrorHandler(data)
        self.action_handler: class_ActionHandler.ActionHandler = class_ActionHandler.ActionHandler(data)
        self.utils: class_Utils.Utils = class_Utils.Utils(data)

        date = datetime.now()
        self.data.tag = f"logs/{datetime.strftime(date, '%d;%m %H-%M-%S')} @ {ctx.author.display_name}"

        if not os.path.exists("./logs"):
            os.makedirs("./logs")
            
        with open(self.data.tag, "x") as file:
            file.close()

    async def format_code(self) -> None:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()))
        await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                             f"Will be formatting: {self.data.code}")

        self.data.code = self.data.code.split("\n")
        print(self.data.code)

        for index, line in enumerate(self.data.code):
            self.data.current_code_index = index
            self.data.str_line = line.strip("\n")
            self.data.list_line = line.split(" ")
            self.data.line_verified = False

        values_to_delete = "", " ", "\n"

        for index in range(len(self.data.code) - 1, -1, -1):
            if self.data.list_line[index] in values_to_delete:
                self.data.list_line.pop(index)

            await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                                 f"Deleted param @ index {index}")

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), None)

    async def proccess_verify_request(self, count_first_line: bool) -> None:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                count_first_line=count_first_line)

        async with (self.ctx.channel.typing()):
            lines_done = 0
            '''try:'''

            await self.format_code()

            # register all labels
            for index, line in enumerate(self.data.code):
                if not count_first_line and index == 0:
                    continue

                if ":" in (label := self.data.list_line[-1]):
                    self.data.labels.append(label.strip(":"))
                    await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                                         f"Registered a label \"{label}\" in line {index}")

            # for all lines to be verified
            for index, line in enumerate(self.data.code):
                lines_done += 1

                # delete .v from the first line
                if index == 0 and not count_first_line:
                    continue

                if len(self.data.list_line) < 1:
                    await self.utils.add_line_to_result("⬛")
                    continue

                print(self.data.list_line)
                if (action_name := self.data.list_line[0]) in self.action_handler.actions:
                    action_done = await self.action_handler.actions[action_name]()

                    if action_done:
                        await self.utils.add_line_to_result("🟩")

                    else:
                        await self.utils.add_line_to_result("🟥")
                        self.data.errored = True
                        self.data.lines_errored.append(self.data.current_code_index)

                elif "#" in self.data.list_line[0]:
                    await self.utils.add_line_to_result("🟦")

                elif all(znak.isspace() for znak in self.data.list_line) or \
                        self.data.list_line == ['']:
                    await self.utils.add_line_to_result("⬛")

                elif ":" in self.data.list_line[-1] and len(self.data.list_line) == 1:
                    await self.utils.add_line_to_result("🟪")

                elif "!--" in self.data.list_line[0]:
                    await self.utils.add_line_to_result("⬜")

                else:
                    await self.error_handler.template(0, "Invalid action")

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
