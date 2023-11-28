from Code_Validator import Data, LogHandler
import inspect


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
