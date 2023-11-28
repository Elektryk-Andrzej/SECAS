import Data
import inspect
import LogHandler
import Utils


class VerdictHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data
        self.utils: Utils.Utils = data.utils_object
        self.logs: LogHandler.LogHandler = data.log_handler_object

    async def error_template(self, line_index: int, reason: str) -> bool:
        """
        Formats a line by adding arrows around a malformed parameter and automatically creates a line verdict

        :param line_index: line index to report as malformed
        :param reason: the reason why it is malformed
        :return: bool
        """
        self.data.errored = True

        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            reason=reason
        )

        line_copy = self.data.line.copy()
        line_copy[line_index] = f"▶ {line_copy[line_index]} ◀"
        line_to_print = ' '.join(line_copy)

        await self.line_verdict(self.data.LineVerdictType().ERRORED,
                                line_to_print,
                                reason)

        await self.logs.close(True)
        return True

    async def error_invalid_min_length(self, number_missing: int) -> bool:
        """
        Formats a line by adding three underscors where parameters are missing and automatically creates a line verdict

        :param number_missing: number of parameters missing
        :return: bool
        """
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            number_missing=number_missing
        )

        self.data.line_errored = True

        reason = f"Missing required arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        line_copy = self.data.line.copy()
        line_to_print = f"{' '.join(line_copy)} ▶ {missing_arguments}◀"

        await self.line_verdict(self.data.LineVerdictType().ERRORED,
                                line_to_print,
                                reason)

        await self.logs.close(True)
        return True

    async def error_invalid_max_length(self, past_max_length: int) -> bool:
        """
        Formats a line by adding arrows around a malformed parameters and automatically creates a line verdict

        :param past_max_length: number of parameters that exceed the maximum amount possible
        :return: bool
        """
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            past_max_length=past_max_length
        )

        self.data.line_errored = True

        if past_max_length == 1:
            await self.error_template(-1, "Unexpected arguments")

        line_copy = self.data.line.copy()
        reason = f"Unknown arguments | {past_max_length}"
        start_index = len(line_copy) - past_max_length

        line_copy[start_index], line_copy[-1] = \
            f"▶ {line_copy[start_index]}", f"{line_copy[-1]} ◀"

        line_to_print = ' '.join(line_copy)

        await self.line_verdict(self.data.LineVerdictType().ERRORED,
                                line_to_print,
                                reason=reason)

        await self.logs.close(True)
        return True

    async def line_verdict(self,
                           verdict_type: Data.Data.LineVerdictType,
                           line_to_print: str or None = None,
                           reason: str or None = None) -> bool:
        """
        Set a verdict for the line with LineVerdictType attributes and format it for later use

        :return: None
        """
        await self.logs.open(
            inspect.getframeinfo(inspect.currentframe()),
            verdict_type=verdict_type
        )

        if self.data.line_verdict_set:
            await self.logs.log(f"Request denied, a verdict has already been set for line {self.data.line}")
            await self.logs.close(False)
            return False

        self.data.line_verdict_set = True

        normal_line = " ".join(self.data.line)

        color: str
        if verdict_type is self.data.LineVerdictType().ERRORED:
            color = "🟥"

        elif verdict_type is self.data.LineVerdictType().PASSED:
            color = "🟩"

        elif verdict_type is self.data.LineVerdictType().FLAG:
            color = "⬜"

        elif verdict_type is self.data.LineVerdictType().COMMENT:
            color = "🟦"

        elif verdict_type is self.data.LineVerdictType().LABEL:
            color = "🟪"

        elif verdict_type is self.data.LineVerdictType().EMPTY:
            color = "⬛"

        else:
            await self.logs.log("No verdict type provided")
            color = "🟧"
            line_to_print = "ERROR"
            reason = "ERROR"

        self.data.processed_lines.append([
            color, normal_line, line_to_print, reason, self.data.code_index
        ])

        await self.logs.close(True)
        return True
