import os


def delete_logs() -> None:
    for filename in os.listdir("../Logs"):
        os.remove(os.path.join("../Logs/", filename))


if __name__ == "__main__":
    delete_logs()
