import class_DataHandler
import class_ErrorHandler
import discord
import inspect


class Utils:
    def __init__(self, data: class_DataHandler.DataHandler):
        self.data = data

    # Get a value from the line list, report error if outside of range
    async def get_str_from_line(self, line_index) -> str:
        try:
            return str(self.data.list_line[line_index])

        except IndexError:
            await (class_ErrorHandler.ErrorHandler(self.data).
                   secas_error(line_index,
                               f"Tried to access a value outside of range (`{line_index}`), "
                               f"The last value was granted instead (`{str(self.data.list_line[-1])}`). "
                               f"Please report this error to {self.data.andrzej_ping}"))
            return str(self.data.list_line[-1])

    @staticmethod
    async def strip_brackets(val: str) -> str:
        return val.replace("{", "").replace("}", "")

    async def log(self, context: inspect.getframeinfo(inspect.currentframe()), reason: str) -> None:
        """
        Basic log method.
        Must be used after a log_new_inst method for log indent to be correct.

        :param context: inspect.getframeinfo(inspect.currentframe())
        :param reason: Reason of the log
        :return: None
        """

        try:
            log_depth: str = self.data.log_depth_char * self.data.log_depth

            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} {context.function} (@ {context.lineno}) - {reason} \n")

        except AttributeError as e:
            log_depth: str = self.data.log_depth_char * self.data.log_depth

            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} {reason} (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.tag, "a") as file:
                file.write(f"---> ERROR ({e})\n")

    async def log_new_inst(self, context, **kwargs):
        """
        

        :param context:
        :param kwargs:
        :return:
        """
        self.data.log_depth += 1
        log_depth: str = self.data.log_depth_char * self.data.log_depth
        kwargs_formatted: str = ""

        try:
            for i in kwargs.items():
                arg, val = i
                val_type_formatted: str = str(type(val)).strip('<class ').strip('>')

                kwargs_formatted += f"{log_depth} -> {arg}: {val} ({val_type_formatted})\n"

            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} new instance {context.function} with args:\n")
                file.write(f"{kwargs_formatted}")

        except AttributeError as e:
            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} new inst (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.tag, "a") as file:
                file.write(f"---> ERROR ({e})\n")

    async def log_close_inst(self, context, output):
        log_depth: str = self.data.log_depth_char * self.data.log_depth

        try:
            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} closed instance {context.function} (@ {context.lineno}) with {output}\n")
                return output

        except AttributeError as e:
            with open(self.data.tag, "a") as file:
                file.write(f"{log_depth} returned {output} (clsd inst | AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.tag, "a") as file:
                file.write(f"---> ERROR ({e})\n")

        finally:
            self.data.log_depth -= 1

    # Format all of the data and add it into a list, from which it will be assembled into an embed
    async def add_line_to_result(self, emoji: str):
        if emoji == "⬛":
            to_append = f"`{len(self.data.processed_lines) + 1}`{emoji}"
            self.data.processed_lines.append(to_append)
            return

        to_append = f"`{len(self.data.processed_lines) + 1}`{emoji}` {self.data.str_line} `"
        self.data.processed_lines.append(to_append)

    # Idk why i did this, it doesnt make anything easier
    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)
