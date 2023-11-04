import Data
import discord
import inspect


class Utils:
    def __init__(self, data: Data.Data):
        """
        Contains the most basic and universal functions,
        ment to be accessed from anywhere with no problems.
        """

        self.data = data

    async def get_str_from_line(self, line_index) -> str:
        """
        Safely get a value form code with provided index, return the last index if out of range

        - no changes needed

        :param line_index: index to get from the line
        :return: str value of the provided line index
        """

        await self.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                line_index=line_index)

        output: str

        try:
            output = str(self.data.line[line_index])

        except IndexError:
            output = str(self.data.line[-1])
            await self.log(inspect.getframeinfo(inspect.currentframe()),
                           "Specified line index is out of range, returned the last index")

        return await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                         output)

    async def strip_brackets(self, val: str) -> str:
        """
        Strip brackets form the provided value.

        - no changes needed

        :param val: str value to remove brackets from
        :return: str value without brackets
        """

        await self.log_new_inst(inspect.getframeinfo(inspect.currentframe()),
                                val=val)

        output = val.replace("{", "").replace("}", "")

        return await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                         output)

    async def log(self, context: inspect.getframeinfo(inspect.currentframe()), reason: str) -> None:
        """
        Basic log method.
        Must be used after a log_new_inst method for log indent to be correct.

        - no changes needed

        :param context: inspect.getframeinfo(inspect.currentframe())
        :param reason: Reason of the log
        :return: None
        """

        log_depth: str = self.data.log_depth_char * self.data.log_depth
        line_number: str = f"@ {context.lineno}"
        prefix: str = f"{line_number} {' ' * int(5 - len(line_number))} {log_depth}"

        try:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} \"{context.function}\" - {reason}\n")

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
        log_depth: str = self.data.log_depth_char * self.data.log_depth
        line_number: str = f"@ {context.lineno}"
        prefix: str = f"{line_number} {' ' * int(5-len(line_number))} {log_depth}"

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
                file.write(f"{log_depth} new inst (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

        self.data.log_depth += 1

    async def log_close_inst(self, context, output):
        """
        Use in the return statement of a method.
        Will change log depth accordingly for better readability.

        - no changes needed

        :param context: inspect.getframeinfo(inspect.currentframe())
        :param output: the value returned by the method
        :return: provided output
        """

        log_depth: str = self.data.log_depth_char * self.data.log_depth
        line_number: str = f"@ {context.lineno}"
        prefix: str = f"{line_number} {' ' * int(5 - len(line_number))} {log_depth}"

        try:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} CLOSE \"{context.function}\" with {output = }\n")
                return output

        except AttributeError as e:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{log_depth} returned {output} (clsd inst | AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

        finally:
            self.data.log_depth -= 1
            return output

    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)

    async def get_line_as_str(self) -> str:
        await self.log_new_inst(inspect.getframeinfo(inspect.currentframe()))
        to_return = " ".join(self.data.line)
        await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()),
                                  to_return)
        return to_return

    async def is_containing_brackets(self, line_index: int) -> bool:

        await self.log_new_inst(inspect.getframeinfo(inspect.currentframe()), line_index=line_index)

        variable = await self.get_str_from_line(line_index)

        if not (variable[0] == "{" and variable[-1] == "}"):
            await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        variable = variable.removeprefix("{").removesuffix("}")

        if "{" in variable or "}" in variable:
            await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()), False)
            return False

        await self.log_close_inst(inspect.getframeinfo(inspect.currentframe()), True)
        return True
