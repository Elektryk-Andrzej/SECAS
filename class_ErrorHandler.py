import class_DataHandler


class ErrorHandler:
    def __init__(self, ctx, data: class_DataHandler.DataHandler):
        self.ctx = ctx
        self.data = data

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