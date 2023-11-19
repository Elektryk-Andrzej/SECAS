import Data
import inspect


class Utils:
    def __init__(self, data: Data.Data):
        """
        Contains the most basic and universal functions,
        meant to be accessed from anywhere with no problems.
        """

        self.data = data

    async def get_str_from_line_index(self, line_index) -> str:
        """
        Safely get a value form code with provided index, return the last index if out of range

        - no changes needed

        :param line_index: index to get from the line
        :return: str value of the provided line index
        """

        await self.log_new_inst(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)

        output: str
        try:
            output = str(self.data.line[line_index])

        except IndexError:
            output = str(self.data.line[-1])
            await self.log("Specified line index is out of range, returned the last index")

        await self.log_return(output)
        return output

    async def log(self, reason: str) -> None:
        """
        Basic log method.
        Must be used after a log_new_inst method for log indent to be correct.

        - no changes needed

        :param reason: Reason of the log
        :return: None
        """

        prefix: str = self.data.log_depth_char * self.data.log_depth

        try:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} - {reason}\n")

        except AttributeError as e:
            log_depth: str = self.data.log_depth_char * self.data.log_depth

            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{log_depth} {reason} (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

    async def log_new_inst(self, context, **kwargs) -> None:
        """
        Use at the beggining of a method.
        Will change log depth accordingly for better readability.

        - no changes needed

        :param context: inspect.getframeinfo(inspect.currentframe())
        :param kwargs: all args provided
        :return: None
        """
        self.data.log_depth += 1
        prefix: str = self.data.log_depth_char * self.data.log_depth

        kwargs_formatted: str = ""

        try:
            for i in kwargs.items():
                arg, val = i
                val_type_formatted: str = str(type(val)).strip('<class ').strip('>')

                kwargs_formatted += f"{prefix} -> {arg}: {val} ({val_type_formatted})\n"

            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                if kwargs != {}:
                    file.write(f"{prefix} NEW \"{context.function}\" with parameters:\n")
                    file.write(f"{kwargs_formatted}")
                else:
                    file.write(f"{prefix} NEW \"{context.function}\"\n")

        except AttributeError as e:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} new inst (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

    async def log_return(self, output):
        """
        Use in the return statement of a method.
        Will change log depth accordingly for better readability.

        - no changes needed

        :param output: the value returned by the method
        :return: provided output
        """

        self.data.log_depth -= 1

        prefix: str = self.data.log_depth_char * self.data.log_depth

        try:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} CLOSED method with output \"{output}\"({type(output)})\"\n")
                return output

        except AttributeError as e:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} returned {output} (clsd inst | AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

        return output

