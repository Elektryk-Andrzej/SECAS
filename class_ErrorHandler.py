import class_DataHandler


class ErrorHandler:
    def __init__(self, data: class_DataHandler.DataHandler):
        self.data = data

    # Used to handle most errors, surrounds the specified line index with arrows
    async def template(self, line_index: int, reason: str):
        self.data.line_errored = True
        self.data.errored = True

        self.data.list_line[line_index] = f"▶ {self.data.list_line[line_index]} ◀"

        line_with_arrows = ' '.join(self.data.list_line)
        to_append = [self.data.current_code_index, line_with_arrows, reason, None]

        self.data.error_reasons.append(to_append)

    # Send a message that something went wrong
    async def secas_error(self, line_index: int, reason: str):
        self.data.critical_error = \
            f"""
            SECAS has experienced a bug:
            `{reason}` | param `{line_index}` @ line `{self.data.current_code_index}`
            """

    # Adds three "_" for each parameter missing, while surrouding them with arrows
    async def invalid_min_length(self, number_missing: int):
        self.data.line_errored = True

        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        to_append = [self.data.current_code_index,
                     f"{self.data.str_line} ▶ {missing_arguments}◀", reason, None]

        self.data.error_reasons.append(to_append)

    # Surrounds all unwanted parameters with arrows
    async def invalid_max_length(self, past_max_length: int):

        # this method needs to have more than 1 argument, if not, redirect to a normal one
        if past_max_length == 1:
            await self.template(-1, "Unexpected arguments | 1")

        self.data.line_errored = True
        reason = f"Unexpected arguments | {past_max_length}"
        start_index = len(self.data.list_line) - past_max_length

        self.data.list_line[start_index], self.data.list_line[-1] = \
            f"▶ {self.data.list_line[start_index]}", f"{self.data.list_line[-1]} ◀"

        line_with_arrows = ' '.join(self.data.list_line)
        to_append = [self.data.current_code_index, line_with_arrows, reason, None]

        self.data.error_reasons.append(to_append)
