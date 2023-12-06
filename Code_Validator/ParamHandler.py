from Code_Validator import Data, LogHandler, Utils, VerdictHandler
import inspect


class ParamHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data
        self.utils: Utils.Utils = data.utils_object
        self.verdict: VerdictHandler.VerdictHandler = data.verdict_handler_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

    async def is_valid_mode(self,
                            line_index: int,
                            *,
                            possible_modes: tuple or list,
                            required: bool = True) -> bool:

        if not required and not await self._is_line_index_present(line_index):
            return True

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            possible_modes=possible_modes
        )

        possible_modes = [possible_mode for possible_mode in possible_modes]
        mode = await self.utils.get_str_from_line_index(line_index)

        if mode in possible_modes:
            await self.logs.close(True)
            return True

        else:
            closest_match = await self.utils.get_closest_match(mode, possible_modes)
            await self.verdict.error_template(
                line_index,
                f"Invalid mode",
                closest_match
            )
            await self.logs.close(False)
            return False

    async def is_non_se_variable(self,
                                 line_index: int,
                                 *,
                                 var_type: object,
                                 required: bool = True,
                                 other_syntax_allowed: tuple = None) -> bool:

        """
        Handles all non-standard variables, like doors, rooms, roles etc.
        
        :param line_index: 
        :param var_type: things like Data.Data.ExampleType
        :param required:
        :param other_syntax_allowed:
        :return: bool
        """

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            var_type=var_type,
            required=required,
            other_syntax_allowed=other_syntax_allowed
        )

        if not required and not await self._is_line_index_present(line_index):
            await self.logs.close(True)
            return True

        variable = await self.utils.get_str_from_line_index(line_index)

        match var_type:
            case Data.Data.Room:
                reason = "Invalid room"
                group = Data.Data.Room.rooms

            case Data.Data.Item:
                reason = "Invalid item"
                group = Data.Data.Item.items

            case Data.Data.Effect:
                reason = "Invalid effect"
                group = Data.Data.Effect.effects

            case Data.Data.Role:
                reason = "Invalid role"
                group = Data.Data.Role.roles

            case Data.Data.Door:
                reason = "Invalid door"
                group = Data.Data.Door.doors

            case Data.Data.SpawnPosition:
                reason = "Invalid position"
                group = Data.Data.SpawnPosition.positions

            case _:
                var_type_name: str = f'{var_type=}'.split('=')[0]
                await self.verdict.error_template(
                    line_index,
                    f"SECAS doesn't support {var_type_name}",
                    verdict_type=self.data.LineVerdict.NOT_CHECKABLE
                )
                await self.logs.close(False)
                return False

        if other_syntax_allowed is not None:
            if variable in other_syntax_allowed:
                await self.logs.close(True)
                return True

        if variable in group:
            await self.logs.close(True)
            return True

        closest_match: str = await self.utils.get_closest_match(variable, group)
        await self.verdict.error_template(line_index, reason, closest_match)
        await self.logs.close(False)
        return False

    async def cant_check(self, line_index: int or None = None) -> bool:
        pass

    async def is_bool(self, line_index, *, required: bool = True) -> bool:
        arg = await self.utils.get_str_from_line_index(line_index)
        possible_args: tuple = ("TRUE", "FALSE", "YES", "NO")

        if not required and not await self._is_line_index_present(line_index):
            await self.logs.close(True)
            return True

        if arg.casefold() in [possible_arg.casefold() for possible_arg in possible_args]:
            await self.logs.close(True)
            return True

        closest_match: str = await self.utils.get_closest_match(arg, possible_args)
        await self.verdict.error_template(line_index, f"Invalid bool | Did you mean {closest_match}?")
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

        elif len(self.data.labels) > 0:
            closest_match: str = await self.utils.get_closest_match(parameter, self.data.labels)
            await self.verdict.error_template(line_index, f"Invalid label | Did you mean {closest_match}?")
        else:
            await self.verdict.error_template(line_index, "No labels registered")

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

        if math_supported:
            await self.logs.close(True)
            return True

        to_be_number = await self.utils.get_str_from_line_index(line_index)

        try:
            if min_value <= var_type(eval(to_be_number)) <= max_value:

                await self.logs.close(True)
                return True

        except TypeError or Exception:
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

    # With dedication to saskyc
    @staticmethod
    async def sex() -> str:
        return "sex"
