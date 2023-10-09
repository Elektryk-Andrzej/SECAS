from datetime import *
import discord
import class_DataHandler
import class_ActionHandler
import class_ErrorHandler
import class_Utils


class IOHandler:
    def __init__(self, data: class_DataHandler.DataHandler, ctx, bot):
        self.data: class_DataHandler.DataHandler = data
        self.bot = bot
        self.ctx = ctx
        self.error_handler: class_ErrorHandler.ErrorHandler = class_ErrorHandler.ErrorHandler(data)
        self.action_handler: class_ActionHandler.ActionHandler = class_ActionHandler.ActionHandler(data)
        self.utils: class_Utils.Utils = class_Utils.Utils(data)

        date = datetime.now()
        self.data.tag = f"{datetime.strftime(date, '%d;%m %H-%M-%S')} @ {ctx.author.display_name}"

        with open(self.data.tag, "x") as file:

            file.close()

    async def delete_empty_params(self) -> None:
        index_to_pop = []

        for index, value in enumerate(self.data.line_in_list):
            if value == "" or value == " ":
                index_to_pop.append(index)

        for index in range(len(index_to_pop)-1, -1, -1):
            self.data.line_in_list.pop(index)

    async def proccess_verify_request(self, count_first_line: bool) -> None:
        await self.utils.log(f"Initialized ver request as {self.data.tag}")

        async with (self.ctx.channel.typing()):
            lines_done = 0
            '''try:'''
            self.data.code = self.data.code.split("\n")

            await self.utils.log(f'Recorded code as:\n {[await self.utils.log(i) for i in self.data.code]}')

            # register all labels
            for index, line in enumerate(self.data.code):
                self.data.line_in_list = line.split(" ")
                self.data.line_in_list[-1].strip("\n")

                if index == 0 and len(self.data.line_in_list) > 1 and \
                        self.data.line_in_list[0].startswith("."):
                    self.data.line_in_list.pop(0)

                if ":" in (label := self.data.line_in_list[-1]):
                    self.data.labels.append(label.strip(":"))

            # for all lines to be verified
            for index, line in enumerate(self.data.code):
                lines_done += 1

                # delete .v from the first line
                if index == 0 and not count_first_line:
                    continue

                self.data.line_processing_index = index
                self.data.line_in_str = line.strip("\n")
                self.data.line_in_list = line.split(" ")
                self.data.line_in_list[-1].strip("\n")
                self.data.line_already_added_to_result = False
                await self.delete_empty_params()

                if (action_name := self.data.line_in_list[0]) in self.action_handler.actions:
                    action_done = await self.action_handler.actions[action_name]()

                    if action_done:
                        await self.utils.add_line_to_result("🟩")

                    else:

                        await self.utils.add_line_to_result("🟥")
                        self.data.errored = True
                        self.data.lines_errored.append(self.data.line_processing_index)

                elif "#" in self.data.line_in_list[0]:
                    await self.utils.add_line_to_result("🟦")

                elif all(znak.isspace() for znak in self.data.line_in_list) or \
                        self.data.line_in_list == ['']:
                    await self.utils.add_line_to_result("⬛")

                elif ":" in self.data.line_in_list[-1] and len(self.data.line_in_list) == 1:
                    await self.utils.add_line_to_result("🟪")

                elif "!--" in self.data.line_in_list[0]:
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
        character_limit = 2000
        color_error = 0xdd2e44
        color_no_error = 0x77b255
        embed_content = ""

        if self.data.errored:
            await self.ctx.reply(embed=await self.utils.create_embed(
                                             f"Errors found: `{len(self.data.error_reasons)}`",
                                             None,
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
                                 None,
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
