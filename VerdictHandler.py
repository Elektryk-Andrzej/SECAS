import DataHandler
import Utils
import inspect


class VerdictHandler:
    def __init__(self, data: DataHandler.Data):
        self.data = data
        self.utils = Utils.Utils(data)

    async def error_template(self, line_index: int, reason: str) -> None:
        """
        Formats a line by adding arrows around a malformed parameter and automatically creates a line verdict

        :param line_index: line index to report as malformed
        :param reason: the reason why it is malformed
        :return: None
        """
        await self.utils.log_new_inst(
            inspect.getframeinfo(inspect.currentframe()),
            line_index=line_index,
            reason=reason
        )
        self.data.errored = True
        
        line_copy = self.data.line.copy()
        line_copy[line_index] = f"▶ {line_copy[line_index]} ◀"
        line_to_print = ' '.join(line_copy)

        await self.line_verdict(self.data.LineVerdictType.ERRORED,
                                line_to_print,
                                reason)

    async def error_invalid_min_length(self, number_missing: int) -> None:
        """
        Formats a line by adding three underscors where parameters are missing and automatically creates a line verdict

        :param number_missing: number of parameters missing
        :return: None
        """
        self.data.line_errored = True

        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        line_copy = self.data.line.copy()
        line_to_print = f"{' '.join(line_copy)} ▶ {missing_arguments}◀"

        await self.line_verdict(self.data.LineVerdictType.ERRORED,
                                line_to_print,
                                reason)

    # Surrounds all unwanted parameters with arrows
    async def error_invalid_max_length(self, past_max_length: int):

        if past_max_length == 1:
            await self.error_template(-1, "Unexpected arguments | 1")

        self.data.line_errored = True
        reason = f"Unexpected arguments | {past_max_length}"
        start_index = len(self.data.list_line) - past_max_length

        self.data.list_line[start_index], self.data.list_line[-1] = \
            f"▶ {self.data.list_line[start_index]}", f"{self.data.list_line[-1]} ◀"

        line_with_arrows = ' '.join(self.data.list_line)
        to_append = [self.data.current_code_index, line_with_arrows, reason, None]

        self.data.error_reasons.append(to_append)

    async def line_verdict(self,
                           verdict_type: DataHandler.Data.LineVerdictType,
                           line_to_print: str | None = None,
                           reason: str | None = None) -> bool:
        """
        Set a verdict for the line with LineVerdictType attributes and format it for later use

        :return: None
        """
        await self.utils.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                verdict_type=verdict_type)

        if self.data.line_verdict_set:
            await self.utils.log(inspect.getframeinfo(inspect.currentframe()),
                           "Request denied, a verdict has already been set for this line.")
            await self.utils.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                False)
            return False

        self.data.line_verdict_set = True

        if verdict_type is self.data.LineVerdictType.PASSED:
            self.data.processed_lines.append([

            ])
