import logging

logging.basicConfig(level=logging.DEBUG, filename="logs.txt", filemode="w",
                format=f"%(levelname)s | %(message)s", datefmt="%H:%M:%S", encoding="utf8")


def log_func(func):
    def wrapper(*args, **kwargs):
        if args:
            params = f"{args} {kwargs}" if kwargs else args
        elif kwargs:
            params = kwargs
        else:
            params = "None"

        try:
            logging.debug(f'Called: {func.__name__} - {params}')

            result = func(*args, **kwargs)
            return result

        except Exception:
            logging.exception(f'{func.__name__} got fucked')

    return wrapper
