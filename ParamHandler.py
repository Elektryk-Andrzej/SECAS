import Data
import VerdictHandler
import Utils


class ParamHandler:
    def __init__(self, data: Data.Data):
        self.data = data
        self.utils = Utils.Utils(data)
        self.verdict_handler = VerdictHandler.VerdictHandler(data)

    # Register a certain value to a SE variable
    async def register_var(self, name_index: int, value_index: int, *,
                           player_var: bool, everything_in_range: bool = False):

        variable_name = await self.utils.get_str_from_line(name_index)
        variable_name = await self.utils.strip_brackets(variable_name)
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.data.line[value_index:])
        else:
            variable_value = await self.utils.get_str_from_line(value_index)

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
            self.data.custom_variables.append([variable_name, await get_type(), False, variable_value])

        elif player_var:
            self.data.custom_variables.append([variable_name, int, True, variable_value])

        return True

    # Handles all non-standard variables, like doors, rooms, roles etc.
    # Requires to specify a list which is to be checked
    async def is_special_var(self,
                             line_index: int, *, var_type: list,
                             required: bool = True, star_allowed: bool = False) -> bool:
        if not required:
            if len(self.data.line) - 1 < line_index:
                return True

        variable = self.data.line[line_index]

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
            await self.verdict_handler.error_template(line_index, "* usage forbidden | Use other values")
            return False

        if brackets_required and "{" in variable and "}" in variable:
            variable = variable.replace("{", "").replace("}", "")

        elif brackets_required:
            await self.verdict_handler.error_template(line_index, "`{}` required")
            return False

        if variable in var_type:
            return True

        if ":" in variable:
            await self.utils.line_verdict("🔳")
            return True

        await self.verdict_handler.error_template(line_index, reason)
        return False

    async def is_se_var(self, line_index, *, required: bool = True) -> bool:
        if not await self.is_variable_present(line_index) and not required:
            return True

        if not await self.is_containing_brackets(line_index):
            return False

        variable = await self.utils.get_str_from_line(line_index)
        variable = await self.utils.strip_brackets(variable)

        if ":" in variable:
            await self.utils.line_verdict("🔳")
            return True

        if await self.is_variable_defined(var_type=int,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.data.se_variables):
            return True

        if variable == "*":
            await self.verdict_handler.error_template(line_index, "Asterisk usage forbidden")
            return False

        await self.verdict_handler.error_template(line_index, "Invalid SE variable")
        return False

    async def is_bool(self, line_index, *, required: bool = True) -> bool:

        variable = await self.utils.get_str_from_line(line_index)

        if not required and not await self.is_variable_present(line_index):
            return True

        if variable == "TRUE" or variable == "FALSE":
            return True

        for se_var in self.data.se_variables:
            if variable.replace("{", "").replace("}", "") == se_var[0] and se_var[1] is bool:
                return True

        await self.verdict_handler.error_template(line_index, "Invalid TRUE/FALSE argument")
        return False

    async def is_label(self, line_index) -> bool:
        try:
            iterator = await self.utils.get_str_from_line(line_index)

            if iterator in self.data.labels:
                return True

            elif int(iterator):
                await self.verdict_handler.error_template(line_index, f"Detected number | USE LABELS!")
                return False

        except:
            await self.verdict_handler.error_template(line_index, f"Invalid label")
            return False

    async def is_containing_brackets(self, line_index: int) -> bool:

        variable = await self.utils.get_str_from_line(line_index)

        if not (variable[0] == "{" and variable[-1] == "}"):
            return False

        variable = variable.removeprefix("{").removesuffix("}")

        if "{" in variable or "}" in variable:
            return False

        return True

    # Check if len(list) can accommodate a param at the specified index
    async def is_variable_present(self, line_index: int) -> bool:

        action_len = len(self.data.list_line) - 1

        if action_len >= line_index:
            return True
        else:
            return False

    # Check if a variable in a list is present, True if is, False if not
    async def is_variable_defined(self, *,
                                  var_type: type,
                                  line_index: int,
                                  player_var: bool,
                                  var_list: list) -> bool:

        if var_list == self.data.se_variables:
            var_list = self.data.se_variables + self.data.custom_variables

        var_name = await self.utils.get_str_from_line(line_index)
        var_name = await self.utils.strip_brackets(var_name)

        for se_var in var_list:
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

    async def is_variable_specified_type(self,
                                         var_type: type,
                                         line_index: int) -> bool:

        variable = await self.utils.get_str_from_line(line_index)

        try:
            var_type(variable)
            return True
        except:
            return False

    async def is_number(self, line_index: int, var_type: int or float, *,
                        math_supported: bool = False,
                        required: bool = True,
                        min_value: int = float('-inf'),
                        max_value: int = float('inf')) -> bool:

        if (not required) and (not await self.is_variable_present(line_index)):
            return True

        if await self.is_variable_defined(var_type=var_type,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.data.se_variables):

            return True

        if await self.is_variable_specified_type(var_type, line_index):
            return True

        if math_supported:
            await self.utils.line_verdict("🔲")
            return True

        to_be_number = await self.utils.get_str_from_line(line_index)

        try:
            if min_value <= var_type(eval(to_be_number)) <= max_value:
                return True
        except:
            pass

        await self.verdict_handler.error_template(line_index, "Invalid integer number")
        return False

    async def is_required_len(self, min_len: int, max_len) -> bool:
        action_len = len(self.data.list_line) - 1

        if not min_len <= action_len:
            await self.verdict_handler.error_invalid_min_length(abs(action_len - min_len))

            return False

        if max_len is None:
            return True

        if not action_len <= max_len:
            await self.verdict_handler.error_invalid_max_length(action_len - max_len)

            return False

        return True
