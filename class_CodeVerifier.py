import discord
# import re
import logging
import class_DataHandler

logging.basicConfig(level=logging.DEBUG, filename="logs.txt", filemode="w",
                    format=f"%(levelname)s | %(message)s", datefmt="%H:%M:%S", encoding="utf8")
data = class_DataHandler.Data()


class CodeVerifier:
    def __init__(self, ctx, bot, code):
        self.code = code.split("\n")
        self.bot = bot
        self.ctx = ctx


    """
    END OF __init__ SECTION
    
    START OF ERROR HANDLING SECTION
    """

    # Simple reminidng reply
    async def error_no_code(self):
        await self.ctx.reply("No code to check! First line is always ignored.")

    # Used to handle most errors, surrounds the specified line index with arrows
    async def error_template(self, line_index, reason):
        self.line_processing_list[line_index] = f"▶ {self.line_processing_list[line_index]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        to_append = [self.line_processing_index, error_with_arrows, reason]

        self.error_reasons.append(to_append)

    # Adds three "_" for each parameter missing, while surrouding them with arrows
    async def error_invalid_min_length(self, number_missing: int):
        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        to_append = [self.line_processing_index,
                     f"{self.line_processing_str} ▶ {missing_arguments}◀", reason]

        self.error_reasons.append(to_append)

    # Surrounds all unwanted parameters with arrows
    async def error_invalid_max_length(self, past_max_length: int):
        reason = f"Unexpected arguments | {past_max_length}"

        start_index = len(self.line_processing_list) - past_max_length

        self.line_processing_list[start_index], self.line_processing_list[-1] = \
            f"▶ {self.line_processing_list[start_index]}", f"{self.line_processing_list[-1]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)

        to_append = [self.line_processing_index, error_with_arrows, reason, None]

        self.error_reasons.append(to_append)

    """
    END OF ERROR HANDLING SECTION
    
    START OF OUTPUT MANAGEMENT SECTION
    """

    # Format all of the data and add it into a list, from which it will be assembled into an embed
    async def add_line_to_result(self, emoji: str):
        if emoji == "⬛":
            to_append = f"`{len(self.processed_lines) + 1}`{emoji}"
            self.processed_lines.append(to_append)
            return

        to_append = f"`{len(self.processed_lines) + 1}`{emoji}` {self.line_processing_str} `"
        self.processed_lines.append(to_append)

    # Idk why i did this, it doesnt make anything easier
    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)

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

    """
    END OF OUTPUT MANAGEMENT SECTION
    
    START OF ACTION SECTION
    
    
    Basic action check schematic:
    
    > Check if param is as it should be
    > If it's good, check the next param, if not, return False
    >> Errors are usually raised in the middle of the "check tree" (things like is_action_required_len),
    >> so operating on bool values is essential to pass the info that something went wrong to lower parts
    > If all params were checked and none returned False, return True
    """




    """
    END OF ACTION SECTION
    
    START OF ACTION HANDLING SECTION
    """

    # Register a certain value to a SE variable
    async def register_variable(self, name_index: int, value_index: int, *,
                                player_var: bool, everything_in_range: bool = False):

        variable_name = await self.get_str_from_line(name_index)
        variable_name = await self.strip_brackets(variable_name)
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.line_processing_list[value_index:])
        else:
            variable_value = await self.get_str_from_line(value_index)

        if not await self.is_containing_brackets(name_index):
            return False

        async def get_type() -> type or bool:
            if variable_value.lower() == "true" or variable_value.lower() == "false":
                return bool

            try:
                int(variable_value)
                return int
            except ValueError:
                pass

            try:
                float(variable_value)
                return float
            except ValueError:
                pass

            try:
                str(variable_value)
                return str
            except ValueError:
                pass

            return False

        if not player_var:
            if not await get_type():
                await self.error_template(variable_value, "Couldn't convert variable to any type")
                return None

            self.custom_variables.append([variable_name, await get_type(), False, variable_value])

        elif player_var:
            self.custom_variables.append([variable_name, int, True, variable_value])

        return True

    # Handles all non-standard variables, like doors, rooms, roles etc.
    # Requires to specify a list which is to be checked
    async def is_param_special_var(self,
                                   line_index: int, *, var_type: list,
                                   required: bool = True, star_allowed: bool = False) -> bool:
        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        variable = self.line_processing_list[line_index]

        if var_type[0] == "DEBUG_ROOM_TYPE":
            reason = "Invalid room variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_ITEM_TYPE":
            reason = "Invalid item variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_EFFECT_TYPE":
            reason = "Invalid effect variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_ROLE_TYPE":
            reason = "Invalid role variable"
            brackets_required = False

        elif var_type[0] == "DEGUG_DOOR_TYPE":
            reason = "Invalid door variable"
            brackets_required = False

        else:
            reason = "UNKNOWN ERROR | CONTACT ANDRZEJ"
            brackets_required = False

        if star_allowed and variable == "*":
            return True
        elif not star_allowed and variable == "*":
            await self.error_template(line_index, "* usage forbidden | Use other values")
            return False

        if brackets_required and "{" in variable and "}" in variable:
            variable = variable.replace("{", "").replace("}", "")

        elif brackets_required:
            await self.error_template(line_index, "`{}` required")
            return False

        if variable in var_type:
            return True

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        await self.error_template(line_index, reason)
        return False

    async def is_param_se_var(self, line_index, *, required: bool = True) -> bool:
        if not await self.is_variable_present(line_index) and not required:
            return True

        if not await self.is_containing_brackets(line_index):
            return False

        variable = await self.get_str_from_line(line_index)
        variable = await self.strip_brackets(variable)

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        if await self.is_variable_defined(var_type=int,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.se_variables):
            return True

        if variable == "*":
            await self.error_template(line_index, "Asterisk usage forbidden")
            return False

        await self.error_template(line_index, "Invalid SE variable")
        return False

    async def is_param_bool(self, line_index, *, required: bool = True) -> bool:

        variable = await self.get_str_from_line(line_index)

        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        if variable == "TRUE" or variable == "FALSE":
            return True

        for se_var in self.se_variables:
            if variable.replace("{", "").replace("}", "") == se_var[0] and se_var[1] is bool:
                return True

        await self.error_template(line_index, "Invalid TRUE/FALSE argument")
        return False

    async def is_param_label(self, line_index) -> bool:
        try:
            iterator = await self.get_str_from_line(line_index)

            if iterator in self.labels:
                logging.debug(f"{self.is_param_label.__name__}")
                return True
            elif int(iterator):
                await self.error_template(line_index, f"Detected number | USE LABELS!")
                return False

        except:
            await self.error_template(line_index, f"Invalid label")
            return False

    async def is_containing_brackets(self, line_index: int) -> bool:
        variable = await self.get_str_from_line(line_index)
        if not (variable[0] == "{" and variable[-1] == "}"):
            return False

        variable = variable.removeprefix("{").removesuffix("}")

        if "{" in variable or "}" in variable:
            return False

        return True

    # Check if len(list) can accommodate a param at the specified index
    async def is_variable_present(self, line_index: int) -> bool:
        if len(self.line_processing_list) - 1 >= line_index:
            return True
        else:
            return False

    # Get a value from the line list, report error if outside of range
    async def get_str_from_line(self, line_index) -> str:
        try:
            return str(self.line_processing_list[line_index]).strip()
        except IndexError:
            await self.report_bug(line_index,
                                  "Tried to get a value that's outside of the line."
                                  "Returned the last value in the line instead.")
            return str(self.line_processing_list[-1]).strip()

    # Send a message that something went wrong
    async def report_bug(self, line_index: int, error: str):
        self.ctx.reply(f"""
        The bot has experienced a bug:
        `{error}` | param `{line_index}` @ line `{self.line_processing_index}`
        """)

    @staticmethod
    async def strip_brackets(val: str) -> str:
        return val.replace("{", "").replace("}", "")

    # Check if a variable in a list is present, True if is, False if not
    async def is_variable_defined(self, *, var_type: type, line_index: int, player_var: bool, var_list: list) -> bool:
        if var_list == self.se_variables:
            var_list = self.se_variables + self.custom_variables

        var_name = await self.get_str_from_line(line_index)
        var_name = await self.strip_brackets(var_name)

        for se_var in var_list:
            print(se_var)
            # Skip check if name is not the same, or if variable is a player var or not
            if not var_name == se_var[0] or not se_var[2] == player_var:
                continue

            # Check variable type
            if se_var[1] == var_type:
                return True

            # Try to force the value into a requested one (only possible with custom variables)
            if len(se_var) > 3:
                try:
                    var_type(se_var[3])
                    return True
                except:
                    continue

        return False

    async def is_variable_specified_type(self, var_type: type, line_index: int):
        variable = await self.get_str_from_line(line_index)

        try:
            var_type(variable)
            return True
        except:
            return False

    async def is_param_number(self, line_index: int, var_type: int or float, *,
                              math_supported: bool = False,
                              required: bool = True,
                              min_value: int = float('-inf'),
                              max_value: int = float('inf')) -> bool:

        if (not required) and (not await self.is_variable_present(line_index)):
            return True

        if await self.is_variable_defined(var_type=var_type,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.se_variables):
            return True

        if await self.is_variable_specified_type(var_type, line_index):
            return True

        if math_supported:
            await self.add_line_to_result("🔲")
            return True

        to_be_number = await self.get_str_from_line(line_index)

        try:
            if min_value <= var_type(eval(to_be_number)) <= max_value:
                return True
        except:
            pass

        await self.error_template(line_index, "Invalid integer number")
        return False

    async def is_action_required_len(self, min_len: int, max_len) -> bool:
        if not min_len <= len(self.line_processing_list) - 1:
            await self.error_invalid_min_length(abs(len(self.line_processing_list) - 1 - min_len))

            return False

        if max_len is not None:
            if not len(self.line_processing_list) - 1 <= max_len:
                await self.error_invalid_max_length(len(self.line_processing_list) - 1 - max_len)

                return False

        return True
