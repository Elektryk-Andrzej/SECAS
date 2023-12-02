import dataclasses
import pprint


@dataclasses.dataclass
class PointerCharacters:
    up_right: str = "└"
    right_down_left: str = "┬"
    up_down: str = "│"
    arrow_right: str = "»"
    right_down: str = "┌"
    right_left: str = "─"
    up_right_down: str = "├"
    up_right_down_left: str = "┼"
    arrow_left: str = "«"
    up_right_left: str = "┴"


class LabelVisualiser:
    def __init__(self):
        self.char = PointerCharacters
        self.labels: dict = {}
        self.matrix: list = []
        self.connections: dict = {}
        self.script: list = ["SIX:", "NINE:", ":"]

    def format_script(self, script) -> None:
        self.script = script.splitlines()

    def set_matrix(self, rows: int or None = None, columns: int or None = None) -> None:

        for index in range(len(self.script) if not rows else rows):
            column: list = []

            for _ in range(len(self.labels)*2 if not columns else columns):
                column.append(None)

            self.matrix.append(column)

        print(self.matrix)

    @staticmethod
    def _is_primary_column(row_index: int) -> bool:
        return True if row_index % 2 == 1 else False

    def _create_pointer_start_row(self, start_index, row_index, pointer_column, inverted):
        for column_index, column in enumerate(self.matrix[start_index]):

            # Add heading arrow
            if (column_index == 0 or not self._is_primary_column(column_index)) and column is None:
                self.matrix[row_index][column_index] = self.char.arrow_left

            # Add entry "┌" if reached target column
            elif column_index == pointer_column:
                if column is self.char.up_down:
                    self.matrix[row_index][column_index] = self.char.up_right_down

                elif column is self.char.arrow_left:
                    self.matrix[row_index][column_index] = (
                        self.char.right_down_left if not inverted else self.char.up_right_left
                    )

                else:
                    self.matrix[row_index][column_index] = (
                        self.char.right_down if not inverted else self.char.up_right
                    )

                break

            # Add arrow if target column is farther
            elif self._is_primary_column(column_index) and column is None:
                self.matrix[row_index][column_index] = self.char.arrow_left

            # Change from "┌" to "┬" if reached "┌" but not target column
            elif column is self.char.right_down:
                self.matrix[row_index][column_index] = (
                    self.char.right_down_left if not inverted else self.char.up_right_left
                )

    def _create_pointer_end_row(self, end_index, row_index, pointer_column, inverted):
        for column_index, column in enumerate(self.matrix[end_index]):
            if not column_index <= pointer_column:
                continue

            if column_index == pointer_column:
                if column is self.char.up_right or column is self.char.right_down:
                    self.matrix[row_index][pointer_column] = self.char.up_right_down

                elif column is self.char.up_right_down:
                    break

                else:
                    self.matrix[row_index][pointer_column] = (
                        self.char.up_right if not inverted else self.char.right_down
                    )

            elif column is None:
                self.matrix[row_index][column_index] = self.char.arrow_right

    def create_pointer(self, start_index: int, end_index: int) -> bool:
        if end_index < start_index:
            inverted: bool = True
        else:
            inverted: bool = False

        pointer_column = self._get_and_register_lowest_column(start_index, end_index)

        if start_index == end_index:
            return False

        for row_index in range(len(self.matrix)):
            if not inverted and not start_index <= row_index <= end_index:
                continue
            elif inverted and not start_index >= row_index >= end_index:
                continue

            if row_index == start_index:
                result = (
                    self._create_pointer_start_row(
                        start_index,
                        row_index,
                        pointer_column,
                        inverted
                    )
                )

                if result is False:
                    return False

            elif row_index == end_index:
                result = (
                    self._create_pointer_end_row(
                        end_index,
                        row_index,
                        pointer_column,
                        inverted
                    )
                )

                if result is False:
                    return False

            else:
                print(row_index)
                print(pointer_column)
                self.matrix[row_index][pointer_column] = self.char.up_down

        return True

    def _get_and_register_lowest_column(self, start_index: int, end_index: int) -> int:
        if start_index > end_index:
            start_index, end_index = end_index, start_index

        slots_occupying: set = set(range(start_index, end_index+1))

        for key in self.connections.keys():
            val: set = self.connections[key]

            if val & slots_occupying:
                continue

            self.connections[key] = self.connections[key] | slots_occupying
            key_added = key
            break
        else:
            key_added: int = len(self.connections) * 2 + 1
            self.connections[key_added] = slots_occupying

        return key_added

    def register_labels(self):
        for index, line in enumerate(self.script):
            if not line:
                continue

            if str(line).endswith(":") and " " not in line:
                self.labels[str(line).strip(":")] = index
                print("Registeted label")

    def register_redirect_actions(self) -> bool:
        for index, line in enumerate(self.script):
            if line is None:
                continue

            line: list = line.split(" ")
            print(f"{line = }")
            if line[0] == "GOTOIF" and len(line) >= 4:
                print("gotoif detected")
                print(f"{self.create_pointer(index, self.labels[line[1]]) = }")
                print(f"{self.create_pointer(index, self.labels[line[2]]) = }")

            elif line[0] == "GOTO" and len(line) == 2:
                print("goto detected")
                print(f"{self.create_pointer(index, self.labels[line[1]]) = }")

            else:
                print("No actions")

        return True

    def get_result(self) -> list:
        print([row[-1] for row in lv.matrix])
        for i in range(100):
            if any([row[-1] for row in lv.matrix]) is False:
                [row.pop() for row in lv.matrix]
            else:
                break
        else:
            print("fucked")

        for index, row in enumerate(self.matrix):
            row_printable: str = ""

            for column in row[::-1]:
                row_printable += column if column else " "

            yield row_printable


lv = LabelVisualiser()
if input("y/n?") == "y":
    lv.set_matrix(8, 8)
    lv.create_pointer(0, 4)
    lv.create_pointer(6, 4)

    for value in lv.get_result():
        print(f"{value}")
else:
    lv.format_script("GOTOIF SIX NINE x\nSIX:\nNINE:\n\n\nGOTO SIX")
    lv.register_labels()
    lv.set_matrix()
    lv.register_redirect_actions()

    for index, value in enumerate(lv.get_result()):
        print(f"{value} | {lv.script[index]}")






