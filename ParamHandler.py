import Data
import VerdictHandler
import Utils
import inspect


class ParamHandler:
    def __init__(self, data: Data.Data):
        self.data = data
        self.utils = Utils.Utils(data)
        self.verdict_handler = VerdictHandler.VerdictHandler(data)

    # Register a certain value to an SE variable
    async def register_var(self,
                           name_index: int,
                           value_index: int,
                           *,
                           player_var: bool,
                           everything_in_range: bool = False) -> bool:

        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                     name_index=name_index,
                                      value_index=value_index,
                                      player_var=player_var,
                                      everything_in_range=everything_in_range)

        variable_name = await self.utils.get_str_from_line(name_index)
        variable_name = await self.utils.strip_brackets(variable_name)
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.data.line[value_index:])
        else:
            variable_value = await self.utils.get_str_from_line(value_index)

        if not await self.utils.is_containing_brackets(name_index):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
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

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        if not player_var:
            self.data.custom_variables.append([variable_name, await get_type(), False, variable_value])

        elif player_var:
            self.data.custom_variables.append([variable_name, int, True, variable_value])

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
        return True

    # Handles all non-standard variables, like doors, rooms, roles etc.
    # Requires to specify a list which is to be checked
    async def is_special_var(self,
                             line_index: int, *,
                             var_type,
                             required: bool = True,
                             star_allowed: bool = False) -> bool:

        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                      line_index=line_index,
                                      var_type=var_type,
                                      required=required,
                                      star_allowed=star_allowed)

        if not required:
            if len(self.data.line) - 1 < line_index:

                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                return True

        variable = await self.utils.get_str_from_line(line_index)
        variable = variable.casefold()

        if hasattr(Data.Data.RoomType, var_type):
            reason = "Invalid room variable"
            brackets_required = False

        elif hasattr(Data.Data.ItemType, var_type):
            reason = "Invalid item variable"
            brackets_required = False

        elif hasattr(Data.Data.EffectType, var_type):
            reason = "Invalid effect variable"
            brackets_required = False

        elif hasattr(Data.Data.RoomType, var_type):
            reason = "Invalid role variable"
            brackets_required = False

        elif hasattr(Data.Data.DoorType, var_type):
            reason = "Invalid door variable"
            brackets_required = False

        else:
            reason = "Unknown variable"
            brackets_required = False

        if star_allowed and variable == "*":
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        elif not star_allowed and variable == "*":
            await self.verdict_handler.error_template(line_index, "\"*\" usage forbidden")

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        if brackets_required and "{" in variable and "}" in variable:
            variable = await self.utils.strip_brackets(variable)

        elif brackets_required:
            await self.verdict_handler.error_template(line_index, "`{}` required")

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        if variable in var_type:

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if ":" in variable:

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        await self.verdict_handler.error_template(line_index, reason)

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
        return False

    async def is_se_var(self, line_index, *, required: bool = True) -> bool:

        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                      line_index=line_index,
                                      required=required)

        if not await self.is_variable_present(line_index) and not required:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if not await self.utils.is_containing_brackets(line_index):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        variable = await self.utils.get_str_from_line(line_index)
        variable = await self.utils.strip_brackets(variable)

        if ":" in variable:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if await self.is_variable_defined(
            var_type=int,
            line_index=line_index,
            player_var=True,
            var_list=self.data.SEVariable.se_variables
        ):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        await self.verdict_handler.error_template(line_index, "Invalid SE variable")
        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
        return False

    async def is_bool(self, line_index, *, required: bool = True) -> bool:

        variable = await self.utils.get_str_from_line(line_index)

        if not required and not await self.is_variable_present(line_index):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if variable.casefold() == "true" or variable.casefold() == "false":
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        for se_var in self.data.SEVariable.se_variables:
            if await self.utils.strip_brackets(variable) == se_var[0] and se_var[1] is bool:

                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                return True

        await self.verdict_handler.error_template(line_index, "Invalid TRUE/FALSE argument")
        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
        return False

    async def is_label(self, line_index: int) -> bool:

        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index
        )

        try:
            iterator = await self.utils.get_str_from_line(line_index)

            if iterator in self.data.labels:
                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                return True

            elif int(iterator):
                await self.verdict_handler.error_template(line_index, f"Detected number | USE LABELS!")
                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
                return False

        except:
            await self.verdict_handler.error_template(line_index, f"Invalid label")
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

    # Check if len(list) can accommodate a param at the specified index
    async def is_variable_present(self, line_index: int) -> bool:
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)
        action_len = len(self.data.line) - 1

        if action_len >= line_index:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True
        else:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

    # Check if a variable in a list is present, True if is, False if not
    async def is_variable_defined(self, *,
                                  var_type,
                                  line_index: int,
                                  player_var: bool,
                                  var_list: list) -> bool:

        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            var_type=var_type,
            line_index=line_index,
            player_var=player_var,
            var_list=var_list
        )

        if var_list == self.data.SEVariable.se_variables:
            var_list = self.data.SEVariable.se_variables + self.data.custom_variables

        var_name = await self.utils.get_str_from_line(line_index)
        var_name = await self.utils.strip_brackets(var_name)

        for se_var in var_list:
            # Skip check if name is not the same, or if variable is a player var or not
            if not var_name == se_var[0] or not se_var[2] == player_var:
                continue

            # Check variable type
            if se_var[1] == var_type:
                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                return True

            # Try to force the value into a requested one (only possible with custom variables)
            if len(se_var) > 3:
                try:
                    var_type(se_var[3])
                    await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                    return True
                except:
                    continue

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
        return False

    async def is_variable_specified_type(self,
                                         var_type,
                                         line_index: int) -> bool:
        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            var_type=var_type,
            line_index=line_index
        )

        variable = await self.utils.get_str_from_line(line_index)

        try:
            var_type(variable)
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        except:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

    async def is_number(self,
                        line_index: int,
                        var_type: type[float] | type[int],
                        *,
                        math_supported: bool = False,
                        required: bool = True,
                        min_value: int = float('-inf'),
                        max_value: int = float('inf')) -> bool:

        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            var_type=var_type,
            math_supported=math_supported,
            required=required,
            min_value=min_value,
            max_value=max_value
        )

        if (not required) and (not await self.is_variable_present(line_index)):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if await self.is_variable_defined(
            var_type=var_type,
            line_index=line_index,
            player_var=True,
            var_list=self.data.SEVariable.se_variables
        ):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if await self.is_variable_specified_type(var_type, line_index):
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if math_supported:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        to_be_number = await self.utils.get_str_from_line(line_index)

        try:
            # noinspection PyCallingNonCallable
            if min_value <= var_type(eval(to_be_number)) <= max_value:

                await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
                return True
        except ValueError:
            pass

        await self.verdict_handler.error_template(line_index, "Invalid integer number")
        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
        return False

    async def is_required_len(self, min_len: int, max_len) -> bool:
        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            min_len=min_len,
            max_len=max_len
        )

        action_len = len(self.data.line) - 1

        if not min_len <= action_len:
            await self.verdict_handler.error_invalid_min_length(abs(action_len - min_len))

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        if max_len is None:
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
            return True

        if not action_len <= max_len:
            await self.verdict_handler.error_invalid_max_length(action_len - max_len)

            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
        return True
