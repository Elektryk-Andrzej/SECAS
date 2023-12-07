import os


def delete_logs() -> None:
    for filename in os.listdir("../logs"):
        os.remove(os.path.join("../logs/", filename))


if __name__ == "__main__":
    delete_logs()
