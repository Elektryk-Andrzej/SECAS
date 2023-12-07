from code_validator import Data, LogHandler
import inspect
import difflib


class Utils:
    def __init__(self, data: Data.Data):
        """
        Contains the most basic and universal functions,
        meant to be accessed from anywhere with no problems.
        """

        self.data: Data.Data = data
        self.logs: LogHandler.LogHandler = data.log_handler_object

    async def get_str_from_line_index(self, line_index) -> str:
        """
        Safely get a value form code with provided index, return the last index if out of range

        - no changes needed

        :param line_index: index to get from the line
        :return: str value of the provided line index
        """

        await self.logs.open(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)

        output: str
        try:
            output = str(self.data.line[line_index])

        except IndexError:
            output = str(self.data.line[-1])
            await self.logs.log("Specified line index is out of range, returned the last index")

        await self.logs.close(output)
        return output

    @staticmethod
    async def get_closest_match(value: str, possible_values: list or tuple) -> str:
        if value.upper() in possible_values:
            return value.upper()

        elif value.casefold() in possible_values:
            return value.casefold()

        else:
            return difflib.get_close_matches(value, possible_values, n=1, cutoff=0)[0]
