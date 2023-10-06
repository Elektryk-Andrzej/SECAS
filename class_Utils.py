import class_DataHandler
import class_ErrorHandler


class Utils:
    def __init__(self, data: class_DataHandler.DataHandler):
        self.data = data
        self.error_handler = class_ErrorHandler.ErrorHandler(self.data)

    # Get a value from the line list, report error if outside of range
    async def get_str_from_line(self, line_index) -> str:
        try:
            return str(self.data.line_in_list[line_index])

        except IndexError:
            await (self.error_handler.
                   secas_error(line_index,
                               f"Tried to access a value outside of range (`{line_index}`), "
                               f"The last value was granted instead (`{str(self.data.line_in_list[-1])}`). "
                               f"Please report this error to {self.data.andrzej_ping}"))
            return str(self.data.line_in_list[-1])
