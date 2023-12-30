from script_validator import Data, LogHandler, Utils, VerdictHandler
import inspect


class ParamHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data
        self.utils: Utils.Utils = data.utils_object
        self.verdict: VerdictHandler.VerdictHandler = data.verdict_handler_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

    async def _is_valid_variable_syntax(self, line_index: int, report_error: bool = True) -> bool:
        """
        check if correct variable syntax is used
        """

        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)

        variable = await self.utils.get_str_from_line_index(line_index)

        if not (variable[0] == "{" and variable[-1] == "}"):
            if report_error:
                if not ("{" in variable or "}" in variable):
                    await self.verdict.error_template(line_index, "No brackets provided")
                else:
                    await self.verdict.error_template(line_index, "Malformed brackets")

            await self.logs.close(False)
            return False

        variable = variable[1:-1]

        if "{" in variable or "}" in variable:
            if report_error:
                await self.verdict.error_template(line_index, "Nested variables don't exist")
            await self.logs.close(False)
            return False

        await self.logs.close(True)
        return True

    async def _is_incorrect_caps(self,
                                 line_index: int,
                                 propper_value: str | list | tuple,
                                 report_error: bool = True) -> bool:
        """
        check if a variable has incorrect capitalization
        """

        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)
        variable = await self.utils.get_str_from_line_index(line_index)

        if type(propper_value) is str:

            if variable.casefold() == propper_value.casefold():
                if report_error:
                    await self.verdict.error_template(
                        line_index,
                        "Invalid capitalization",
                        propper_value,
                        self.data.LineVerdict.TYPO,
                        ("Consider changing to ", "")
                    )

                await self.logs.close(True)
                return True

        elif type(propper_value) is tuple or type(propper_value) is list:
            for val in propper_value:

                if variable.casefold() == val.casefold():
                    if report_error:
                        await self.verdict.error_template(
                            line_index,
                            "Invalid capitalization",
                            val,
                            self.data.LineVerdict.TYPO,
                            ("Consider changing to ", "")
                        )

                    await self.logs.close(True)
                    return True

        await self.logs.close(False)
        return False

    async def is_valid_mode(self,
                            line_index: int,
                            *,
                            possible_modes: tuple or list,
                            required: bool = True,
                            report_error: bool = True) -> bool:
        """
        check if param is a valid mode
        """

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

        closest_match = await self.utils.get_closest_match(mode, tuple(possible_modes))

        if await self._is_incorrect_caps(line_index, closest_match, report_error):
            await self.logs.close(False)
            return False

        if report_error:
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
                                 other_syntax_allowed: tuple = None,
                                 report_error: bool = True) -> bool:

        """
        all non-standard variables, like doors, rooms, roles
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

            case Data.Data.DisableKey:
                reason = "Invalid key"
                group = Data.Data.DisableKey.keys

            case Data.Data.Team:
                reason = "Invalid team"
                group = Data.Data.Team.teams

            case Data.Data.Candy:
                if report_error:
                    await self.verdict.mark_uncheckable_parameters(line_index)
                return True

            case _:
                if report_error:
                    await self.verdict.error_template(
                        line_index,
                        f"Can't check",
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

        closest_match: str = await self.utils.get_closest_match(
            variable,
            group + other_syntax_allowed if other_syntax_allowed else group
        )

        if await self._is_incorrect_caps(line_index, group, report_error):
            await self.logs.close(False)
            return False

        if report_error:
            await self.verdict.error_template(line_index, reason, closest_match)
        await self.logs.close(False)
        return False

    async def mark_as_uncheckable(self, line_index: int, to_line_end: bool = False) -> None:
        """
        mark this as something that we cant check (a lot of stuff lol)
        """

        await self.verdict.mark_uncheckable_parameters(line_index, to_line_end)
        pass

    async def is_se_variable(self, line_index: int, report_error: bool = True) -> bool:
        """
        check if param is a variable
        """

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index
        )

        param = await self.utils.get_str_from_line_index(line_index)

        if param == "*":
            await self.logs.close(True)
            return True

        if await self._is_incorrect_caps(line_index, "ALL", report_error):
            await self.logs.close(False)
            return False

        if not await self._is_valid_variable_syntax(line_index, report_error):
            await self.logs.close(False)
            return False

        if report_error:
            await self.verdict.mark_uncheckable_parameters(
                line_index,
                text_to_replace_with="<var>"
            )

        await self.logs.close(True)
        return True

    async def text(self, start_line_index: int) -> None:
        """
        some text that we dont care about, like broadcast or cassie
        """
        if not await self._is_line_index_present(start_line_index):
            return

        await self.verdict.mark_uncheckable_parameters(start_line_index,
                                                       True,
                                                       "<txt>")
        return

    async def condition(self, start_line_index: int) -> None:
        """
        mark the start point of a condition
        """

        # THUNDERMAKER300 gimme code for this

        if not await self._is_line_index_present(start_line_index):
            return

        await self.verdict.mark_uncheckable_parameters(start_line_index,
                                                       True,
                                                       "<cnd>")
        return

    async def is_bool(self, line_index, *, required: bool = True) -> bool:
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index
        )

        arg: str = await self.utils.get_str_from_line_index(line_index)
        possible_args: tuple = "TRUE", "FALSE"

        if not required and not await self._is_line_index_present(line_index):
            await self.logs.close(True)
            return True

        if arg.casefold() in [possible_arg.casefold() for possible_arg in possible_args]:
            await self.logs.close(True)
            return True

        await self.verdict.mark_uncheckable_parameters(line_index)
        await self.logs.close(True)
        return True

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
            closest_match: str = await self.utils.get_closest_match(parameter, tuple(self.data.labels))
            await self.verdict.error_template(line_index, f"Invalid label", closest_match)
        else:
            await self.verdict.error_template(line_index, "No labels registered")

        await self.logs.close(False)
        return False

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
        """
        is param a number
        """

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
            await self.verdict.mark_uncheckable_parameters(
                line_index,
                True,
                "<mth>"
            )
            await self.logs.close(True)
            return True

        to_be_number = await self.utils.get_str_from_line_index(line_index)
        numbers = '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'

        if var_type is int and all([(char in numbers) for char in to_be_number]):
            await self.logs.close(True)
            return True

        elif var_type is float and all([(char in numbers or char == ".") for char in to_be_number]):
            await self.logs.close(True)
            return True

        if not await self._is_valid_variable_syntax(line_index, False):
            await self.verdict.error_template(
                line_index,
                "Invalid variable syntax",
                footer="(this action doesn't support math)"
            )
            await self.logs.close(False)
            return False

        await self.logs.close(True)
        return True

    async def is_required_len(self, min_len: int, max_len) -> bool:
        """
        does action have all required params
        """
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
    
    async def _strip_brackets(self, val: str) -> str:
        """
        Strip brackets form the provided value
        """

        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), val=val)

        output = val.strip()[1:-1]

        await self.logs.close(output)
        return output

    # With dedication to saskyc
    @staticmethod
    async def sex() -> str:
        return "sex"

    # saskyc momento
    @staticmethod
    async def autism() -> str:
        return "saskyc"
