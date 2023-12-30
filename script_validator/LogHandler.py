from script_validator import Data


class LogHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data

    async def log(self, reason: str) -> None:
        """
        Basic log method.
        Must be used after an open method for log indent to be correct.

        - no changes needed

        :param reason: Reason of the log
        :return: None
        """
        return

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

    async def open(self, context, name: str or None = None, **kwargs) -> None:
        """
        Use at the beggining of a method.
        Will change log depth accordingly for better readability.

        - no changes needed

        :param context: inspect.getframeinfo(inspect.currentframe())
        :param name: name of function, if proivided, "context" argument won't be used
        :param kwargs: all args provided
        :return: None
        """
        return
        self.data.log_depth += 1
        prefix: str = self.data.log_depth_char * self.data.log_depth
        kwargs_formatted: str = ""
        func_name = name if name else context.function

        try:
            for i in kwargs.items():
                arg, val = i

                val_type_formatted: str = str(type(val)).strip('<class ').strip('\'>')
                kwargs_formatted += f"{prefix} -> {arg}: {val} ({val_type_formatted})\n"

            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                if kwargs != {}:
                    file.write(f"{prefix} NEW \"{func_name}\" with parameters:\n")
                    file.write(f"{kwargs_formatted}")
                else:
                    file.write(f"{prefix} NEW \"{func_name}\"\n")

        except AttributeError as e:
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"{prefix} new inst (AttributeError - {e})\n")

        except Exception as e:
            print(f"---> ERROR ({e})")
            with open(self.data.log_file_name, "a", encoding="utf-8") as file:
                file.write(f"---> ERROR ({e})\n")

    async def close(self, output):
        """
        Use in the return statement of a method.
        Will change log depth accordingly for better readability.

        - no changes needed

        :param output: the value returned by the method
        :return: provided output
        """
        return

        prefix: str = self.data.log_depth_char * self.data.log_depth
        output_type: str = str(type(output)).strip('<class ').strip('\'>')

        with open(self.data.log_file_name, "a", encoding="utf-8") as file:
            file.write(f"{prefix} CLOSED method with \"{output}\" ({output_type})\"\n\n")

        self.data.log_depth -= 1
        return output

    '''def log_action(self, f):
        async def wrapper(*args, **kwargs):
            await self.open()
            return await f(*args, **kwargs)

        return wrapper'''
