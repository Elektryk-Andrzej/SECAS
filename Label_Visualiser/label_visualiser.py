
class Siur:
    def __init__(self):

        self.example: str = (
            "GOTOIF NINE SIX\n"
            "SIX:\n"
            "NINE:\n"
            ""
        )
        self.labels: dict = {}
        self.a = "└"
        self.b = "┬"
        self.c = "│"
        self.d = ">"
        self.e = "┌"
        self.f = "─"
        self.g = "├"
        self.h = "┼"
        self.i = "<"
        self.matrix: list = []
        self.connections: dict = {}


siur = Siur()


def set_matrix():
    for index in range(len(siur.example.splitlines())):
        column: list = []

        for i in range(len(siur.labels)*2):
            column.append(i)

        siur.matrix.append(column)

    print(siur.matrix)

def is_primary_row(row_index: int) -> bool:
    return True if row_index % 2 == 1 else False

def is_secondary_row(row_index: int) -> bool:
    return True if row_index % 2 == 0 else False

def add_connection(start_index, label):
    label_path_depth = int(siur.labels[label]) * 2
    print(f"{label_path_depth = } for {label = }")

    for index, row in enumerate(siur.matrix[start_index]):
        pass


def create_pointer(start_index: int, end_index: int, pointer_column: int) -> bool:
    if start_index == end_index:
        return False

    for column_index in range(len(siur.matrix)):
        if not start_index <= column_index <= end_index:
            continue

        if column_index == start_index:
            for row_index, row in enumerate(siur.matrix[column_index]):

                if row_index == 0 and not row:
                    siur.matrix[column_index][row_index] = "<"








def register_labels():
    for index, line in enumerate(siur.example.splitlines()):
        print(f"{index = } | {line = }")
        if not line:
            continue

        if str(line).endswith(":") and " " not in line:
            siur.labels[str(line).strip(":")] = index
            print(siur.labels)


def get_action():
    for index, line in enumerate(siur.example.splitlines()):
        print(f"{index = } | {line = }")
        if not line:
            continue

        if not str(line).startswith("GOTOIF"):
            continue

        line_as_list: list = line.split(" ")

        if len(line_as_list) < 3:
            print("gotoif invalid structure")
            continue

        add_connection(index, line_as_list[1])
        add_connection(index, line_as_list[2])


register_labels()
set_matrix()
create_pointer(2, 3)





