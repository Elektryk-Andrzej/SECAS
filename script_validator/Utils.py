from script_validator import Data
import difflib


class Utils:
    def __init__(self, data: Data.Data):
        """
        Contains the most basic and universal functions,
        meant to be accessed from anywhere with no problems.
        """

        self.data: Data.Data = data

    async def get_str_from_line_index(self, line_index) -> str:
        """
        Safely get a value form code with provided index, return the last index if out of range

        - no changes needed

        :param line_index: index to get from the line
        :return: str value of the provided line index
        """

        output: str
        try:
            output = str(self.data.line[line_index])

        except IndexError:
            output = str(self.data.line[-1])

        return output

    @staticmethod
    async def get_closest_match(value: str, possible_values: tuple) -> str:
        if value.upper() in possible_values:
            return value.upper()

        elif value.casefold() in possible_values:
            return value.casefold()

        elif value.capitalize() in possible_values:
            return value.capitalize()

        elif value.lower() in possible_values:
            return value.lower()

        else:
            return difflib.get_close_matches(value, possible_values, n=1, cutoff=0)[0]
