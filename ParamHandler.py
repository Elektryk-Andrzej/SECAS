import Data
import inspect

import LogHandler
import Utils
import VerdictHandler


class ParamHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data
        self.utils: Utils.Utils = data.utils_object
        self.verdict: VerdictHandler.VerdictHandler = data.verdict_handler_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

    # Register a certain value to an SE variable
    async def register_var(self,
                           name_index: int,
                           value_index: int,
                           *,
                           player_var: bool,
                           everything_in_range: bool = False) -> bool:

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            name_index=name_index,
            value_index=value_index,
            player_var=player_var,
            everything_in_range=everything_in_range
        )

        variable_name = await self.utils.get_str_from_line_index(name_index)
        variable_name = await self._strip_brackets(variable_name)
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.data.line[value_index:])
        else:
            variable_value = await self.utils.get_str_from_line_index(value_index)

        if not await self._is_containing_brackets(name_index):
            await self.logs.close(False)
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
            
            await self.logs.close(False)
            return False

        if not player_var:
            self.data.custom_variables.append([variable_name, await get_type(), False, variable_value])

        elif player_var:
            self.data.custom_variables.append([variable_name, int, True, variable_value])
        
        await self.logs.close(True)
        return True

    async def is_valid_mode(self,
                            line_index: int,
                            *,
                            possible_modes: tuple or list,
                            case_sensitive: bool = False,
                            required: bool = True) -> bool:

        if not required and not await self._is_line_index_present(line_index):
            return True

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            possible_modes=possible_modes
        )

        if case_sensitive:
            possible_modes = [possible_mode for possible_mode in possible_modes]
            mode = await self.utils.get_str_from_line_index(line_index)
        else:
            possible_modes = [possible_mode.casefold() for possible_mode in possible_modes]
            mode = str(await self.utils.get_str_from_line_index(line_index)).casefold()

        if mode in possible_modes:
            await self.logs.close(True)
            return True

        else:
            await self.verdict.error_template(line_index, "Invalid mode")
            await self.logs.close(False)
            return False

    async def is_non_se_variable(self,
                                 line_index: int,
                                 *,
                                 var_type: Data.Data.RoomType or Data.Data.ItemType or
                                 Data.Data.EffectType or Data.Data.RoleType or
                                 Data.Data.DoorType,
                                 required: bool = True,
                                 star_allowed: bool = False) -> bool:

        """
        Handles all non-standard variables, like doors, rooms, roles etc.
        
        :param line_index: 
        :param var_type: things like Data.Data.ExampleType
        :param required:
        :param star_allowed: 
        :return: bool
        """

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            var_type=var_type,
            required=required,
            star_allowed=star_allowed
        )

        if not required:
            if len(self.data.line) - 1 < line_index:

                await self.logs.close(True)
                return True

        variable = await self.utils.get_str_from_line_index(line_index)

        if var_type is Data.Data.RoomType:
            reason = "Invalid room variable"
            brackets_required = False
            group = Data.Data.RoomType.room_types
            other_allowed_syntax = "all"

        elif var_type is Data.Data.ItemType:
            reason = "Invalid item variable"
            brackets_required = False
            group = Data.Data.ItemType.item_types
            other_allowed_syntax = None

        elif var_type is Data.Data.EffectType:
            reason = "Invalid effect variable"
            brackets_required = False
            group = Data.Data.EffectType.effect_types
            other_allowed_syntax = None

        elif var_type is Data.Data.RoleType:
            reason = "Invalid role variable"
            brackets_required = False
            group = Data.Data.RoleType.role_types
            other_allowed_syntax = None

        elif var_type is Data.Data.DoorType:
            reason = "Invalid door variable"
            brackets_required = False
            group = Data.Data.DoorType.door_types
            other_allowed_syntax = None

        elif var_type is Data.Data.SpawnPosition:
            reason = "Invalid spawn position"
            brackets_required = False
            group = Data.Data.SpawnPosition.spawn_positions
            other_allowed_syntax = None

        else:
            reason = "Unknown variable"
            group = [None]
            brackets_required = False
            other_allowed_syntax = None

        if star_allowed and variable == "*":
            await self.logs.close(True)
            return True

        if brackets_required and await self._is_containing_brackets(line_index):
            variable = await self._strip_brackets(variable)

        elif brackets_required and not await self._is_containing_brackets(line_index):
            await self.verdict.error_template(line_index, "Brackets absent or malformed")
            await self.logs.close(False)
            return False

        if other_allowed_syntax and variable.casefold() in other_allowed_syntax:
            await self.logs.close(True)
            return True

        if variable in group or any(variable in _ for _ in group):
            await self.logs.close(True)
            return True

        if ":" in variable:
            await self.verdict.line_verdict(self.data.LineVerdictType.NOT_CHECKABLE)

            await self.logs.close(True)
            return True

        await self.verdict.error_template(line_index, reason)

        await self.logs.close(False)
        return False

    async def is_se_var(self,
                        line_index,
                        *,
                        required: bool = True) -> bool:

        """
        Checks if provided variable is a Scripted Events Language variable.
        (SEL variables use bracket, like player variables)

        :param line_index:
        :param required:
        :return:
        """

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            required=required
        )

        if not await self._is_line_index_present(line_index) and not required:
            await self.logs.close(True)
            return True

        if not await self._is_containing_brackets(line_index):
            await self.logs.close(False)

            await self.verdict.error_template(line_index, "Brackets absent or malformed")
            return False

        variable = await self.utils.get_str_from_line_index(line_index)
        variable = await self._strip_brackets(variable)

        if ":" in variable:
            await self.logs.close(True)
            return True

        if await self._is_variable_defined(
            var_type=int,
            line_index=line_index,
            player_var=True,
            var_list=self.data.SEVariable.se_variables
        ):
            await self.logs.close(True)
            return True

        await self.verdict.error_template(line_index, "Invalid SE variable")
        await self.logs.close(False)
        return False

    async def is_bool(self, line_index, *, required: bool = True) -> bool:

        variable = await self.utils.get_str_from_line_index(line_index)

        if not required and not await self._is_line_index_present(line_index):
            await self.logs.close(True)
            return True

        if variable.casefold() == "true" or variable.casefold() == "false":
            await self.logs.close(True)
            return True

        for se_var in self.data.SEVariable.se_variables:
            if await self._strip_brackets(variable) == se_var[0] and se_var[1] is bool:

                await self.logs.close(True)
                return True

        await self.verdict.error_template(line_index, "Invalid TRUE/FALSE argument")
        await self.logs.close(False)
        return False

    async def is_label(self, line_index: int) -> bool:

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index
        )

        parameter = await self.utils.get_str_from_line_index(line_index)

        if parameter in self.data.labels:
            await self.logs.close(True)
            return True

        await self.verdict.error_template(line_index, "Invalid label")
        await self.logs.close(False)
        return False

    # Check if len(list) can accommodate a param at the specified index
    async def _is_line_index_present(self, line_index: int) -> bool:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)
        action_len = len(self.data.line) - 1

        if action_len >= line_index:
            await self.logs.close(True)
            return True
        else:
            await self.logs.close(False)
            return False

    # Check if a variable in a list is present, True if is, False if not
    async def _is_variable_defined(self, *,
                                   var_type,
                                   line_index: int,
                                   player_var: bool,
                                   var_list: list) -> bool:

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            var_type=var_type,
            line_index=line_index,
            player_var=player_var,
            var_list=var_list
        )

        if var_list == self.data.SEVariable.se_variables:
            var_list = self.data.SEVariable.se_variables + self.data.custom_variables

        var_name = await self.utils.get_str_from_line_index(line_index)
        var_name = await self._strip_brackets(var_name)

        for se_var in var_list:
            # Skip check if name is not the same, or if variable is a player var or not
            if not var_name == se_var[0] or not se_var[2] == player_var:
                continue

            # Check variable type
            if se_var[1] == var_type:
                await self.logs.close(True)
                return True

            # Try to force the value into a requested one (only possible with custom variables)
            if len(se_var) > 3:
                try:
                    var_type(se_var[3])
                    await self.logs.close(True)
                    return True
                except:
                    continue

        await self.logs.close(False)
        return False

    async def is_variable_specified_type(self,
                                         var_type: type,
                                         line_index: int) -> bool:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            var_type=var_type,
            line_index=line_index
        )

        variable = await self.utils.get_str_from_line_index(line_index)

        try:
            var_type(variable)
            await self.logs.close(True)
            return True

        except:
            await self.logs.close(False)
            return False

    async def is_number(self,
                        line_index: int,
                        var_type: type[float] or type[int],
                        *,
                        math_supported: bool = False,
                        required: bool = True,
                        min_value: int = float('-inf'),
                        max_value: int = float('inf')) -> bool:

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            var_type=var_type,
            math_supported=math_supported,
            required=required,
            min_value=min_value,
            max_value=max_value
        )

        if (not required) and (not await self._is_line_index_present(line_index)):
            await self.logs.close(True)
            return True

        if await self._is_variable_defined(var_type=var_type,
                                           line_index=line_index,
                                           player_var=True,
                                           var_list=self.data.SEVariable.se_variables):

            await self.logs.close(True)
            return True

        if await self.is_variable_specified_type(var_type, line_index):
            await self.logs.close(True)
            return True

        if math_supported:
            await self.logs.close(True)
            return True

        to_be_number = await self.utils.get_str_from_line_index(line_index)

        try:
            # noinspection PyCallingNonCallable
            if min_value <= var_type(eval(to_be_number)) <= max_value:

                await self.logs.close(True)
                return True
        except ValueError:
            pass

        await self.verdict.error_template(line_index, "Invalid number")
        await self.logs.close(False)
        return False

    async def is_required_len(self, min_len: int, max_len) -> bool:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            min_len=min_len,
            max_len=max_len
        )

        action_len = len(self.data.line) - 1

        if not min_len <= action_len:
            await self.verdict.error_invalid_min_length(abs(action_len - min_len))

            await self.logs.close(False)
            return False

        if max_len is None:
            await self.logs.close(True)
            return True

        if not action_len <= max_len:
            await self.verdict.error_invalid_max_length(action_len - max_len)

            await self.logs.close(False)
            return False

        await self.logs.close(True)
        return True
    
    async def _is_containing_brackets(self, line_index: int) -> bool:
        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)

        variable = await self.utils.get_str_from_line_index(line_index)

        if not (variable[0] == "{" and variable[-1] == "}"):
            await self.logs.close(False)
            return False

        variable = variable.removeprefix("{").removesuffix("}")

        if "{" in variable or "}" in variable:
            await self.logs.close(False)
            return False
        
        await self.logs.close(True)
        return True
    
    async def _strip_brackets(self, val: str) -> str:
        """
        Strip brackets form the provided value.

        :param val: str value to remove brackets from
        :return: str value without brackets
        """

        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), val=val)

        output = val.replace("{", "").replace("}", "")

        await self.logs.close(output)
        return output
