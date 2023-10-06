import class_DataHandler
import class_Utils


class ErrorHandler:
    def __init__(self, data: class_DataHandler.DataHandler):
        self.data = data

    # Used to handle most errors, surrounds the specified line index with arrows
    async def error_template(self, line_index: int, reason: str):
        self.data.line_errored = True

        self.data.line_in_list[line_index] = f"▶ {self.data.line_in_list[line_index]} ◀"

        line_with_arrows = ' '.join(self.data.line_in_list)
        to_append = [self.data.line_processing_index, line_with_arrows, reason, None]

        self.data.error_reasons.append(to_append)

    async def secas_error(self, line_index: int, reason: str):
        pass

    # Adds three "_" for each parameter missing, while surrouding them with arrows
    async def error_invalid_min_length(self, number_missing: int):
        self.data.line_errored = True

        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        to_append = [self.data.line_processing_index,
                     f"{self.data.line_in_str} ▶ {missing_arguments}◀", reason, None]

        self.data.error_reasons.append(to_append)

    # Surrounds all unwanted parameters with arrows
    async def error_invalid_max_length(self, past_max_length: int):
        if past_max_length == 1:  # this method needs to have more than 1 argument, if not, redirect to a normal one
            await self.error_template(-1, "Unexpected arguments | 1")

        self.data.line_errored = True

        reason = f"Unexpected arguments | {past_max_length}"

        start_index = len(self.data.line_in_list) - past_max_length

        self.data.line_in_list[start_index], self.data.line_in_list[-1] = \
            f"▶ {self.data.line_in_list[start_index]}", f"{self.data.line_in_list[-1]} ◀"

        line_with_arrows = ' '.join(self.data.line_in_list)

        to_append = [self.data.line_processing_index, line_with_arrows, reason, None]

        self.data.error_reasons.append(to_append)
