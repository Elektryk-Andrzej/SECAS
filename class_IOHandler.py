import discord
# import re
import class_DataHandler
import class_ActionHandler
import class_ErrorHandler


class IOHandler:
    def __init__(self, data: class_DataHandler.DataHandler, ctx, bot):
        self.data = data
        self.bot = bot
        self.ctx = ctx
        self.error_handler = class_ErrorHandler.ErrorHandler(data)

    async def delete_empty_params(self) -> None:
        index_to_pop = []

        for index, value in enumerate(self.data.line_in_list):
            if value == "" or value == " ":
                index_to_pop.append(index)

        for index in range(len(index_to_pop)-1, -1, -1):
            self.data.line_in_list.remove(index_to_pop[index])

    async def proccess_verify_request(self, count_first_line: bool):
        async with (self.ctx.channel.typing()):
            lines_done = 0
            try:
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

                    action_specified = self.data.line_in_list[0]

                    if action_specified in self.data.actions:
                        action_handler = class_ActionHandler.ActionHandler(self.data)

                        try:
                            action = getattr(action_handler, action_specified)
                        except AttributeError as e:
                            print(f"Action {action_specified} could not be found and executed\n{e}")
                            return

                        if await action:
                            await self.add_line_to_result("🟩")

                        else:
                            await self.add_line_to_result("🟥")
                            self.errored = True

                        continue

                    # comments have blue
                    if "#" in self.data.line_in_list[0]:
                        await self.add_line_to_result("🟦")

                    # blank spaces have black
                    elif all(znak.isspace() for znak in self.data.line_in_list) or \
                            self.data.line_in_list == ['']:
                        await self.add_line_to_result("⬛")

                    # labels have purple
                    elif ":" in self.data.line_in_list[-1] and len(self.data.line_in_list) == 1:
                        await self.add_line_to_result("🟪")

                    # flags have white
                    elif "!--" in self.data.line_in_list[0]:
                        await self.add_line_to_result("⬜")

                    # if nothing matches, then error
                    else:
                        await self.add_line_to_result("🟥")
                        await self.error_handler.error_template(0, "Invalid action")

                        self.errored = True

                if lines_done == 1:
                    await self.ctx.reply("No code found! First line is always ignored.")
                else:
                    await self.send_result_embed()

            except Exception as e:
                await self.ctx.reply("An error occured while generating the overviev.\n"
                                       f"Please report it to {self.data.andrzej_ping}, thank you.\n"
                                       f"`{e}`",
                                     mention_author=False)

        self.data.custom_variables.clear()


    async def send_result_embed(self):
        character_limit = 2000
        color_error = 0xdd2e44
        color_no_error = 0x77b255

        if self.errored:
            embed_number_errors = \
                await self.create_embed(f"Errors found: `{len(self.error_reasons)}`",
                                        None,
                                        color_error)

            await self.ctx.reply(embed=embed_number_errors, mention_author=False)

            for line in self.processed_lines:
                self.embed_content += f"{line}\n"

                if not len(self.embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.create_embed(
                                            None,
                                            self.embed_content,
                                            color_error))
                self.embed_content = ""

            await self.ctx.channel.send(embed=await self.create_embed(
                                        None,
                                        self.embed_content,
                                        color_error))
            self.embed_content = ""

            for line in self.error_reasons:
                self.embed_content += f"### > {line[2]}\n`{line[0]}`🟥` {line[1]} `\n"

                if not len(self.embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.create_embed(
                                            None,
                                            self.embed_content,
                                            color_error))

                self.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=self.embed_content,
                                        color=color_error)

        else:
            await self.ctx.reply(embed=await self.create_embed(
                                 "No errors found!",
                                 None,
                                 color_no_error),
                                 mention_author=False)

            for line in self.processed_lines:
                self.embed_content += f"{line}\n"

                if not len(self.embed_content) > character_limit:
                    continue

                await self.ctx.channel.send(embed=await self.create_embed(
                                            None,
                                            self.embed_content,
                                            color_no_error))
                self.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=self.embed_content,
                                        color=color_no_error)

        final_embed.set_footer(text=f"{self.bot.user.name}by @elektryk_andrzej",
                               icon_url=self.bot.user.avatar)

        await self.ctx.channel.send(embed=final_embed)
