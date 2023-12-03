import dataclasses
from icecream import ic
ic.configureOutput(includeContext=True)


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
        for index in range(len(self.script) if rows is None else rows):
            column: list = []

            for _ in range(len(self.labels)*8 if columns is None else columns):
                column.append(None)

            self.matrix.append(column)

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

                elif column is self.char.right_down and inverted or column is self.char.up_right and not inverted:
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
                self.matrix[row_index][column_index] = self.char.right_down_left

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
                self.matrix[row_index][pointer_column] = self.char.up_down

        return True

    def _get_and_register_lowest_column(self, start_index: int, end_index: int) -> int:

        if start_index > end_index:
            start_index, end_index = end_index, start_index

        def _is_intersecting(pointer_column: int, start_index: int, end_index: int) -> bool:

            for i in range(len(self.connections[pointer_column])):
                space_occupied_start, space_occupied_end = self.connections[pointer_column][i]

                ic(pointer_column, start_index, end_index, space_occupied_start, space_occupied_end)
                if end_index > space_occupied_start and space_occupied_end > start_index:
                    return True

            return False

        if not self.connections:
            self.connections[1] = [[start_index, end_index]]
            ic(self.connections)
            return 1

        for key in self.connections.keys():
            is_intersecting = _is_intersecting(key, start_index, end_index)
            ic(is_intersecting)

            if is_intersecting:
                ic("try get next column")
                continue
            else:
                self.connections[key].append([start_index, end_index])
                ic("added to column", self.connections[key])
                return key
        else:
            key = len(self.connections)*2+1
            self.connections[key] = [[start_index, end_index]]
            ic("no new column available", self.connections[key], key)
            return key

    def register_labels(self):
        for index, line in enumerate(self.script):
            if not line:
                continue

            if str(line).endswith(":") and " " not in line:
                self.labels[str(line).strip(":")] = index

    def register_redirect_actions(self) -> bool:
        for index, line in enumerate(self.script):
            if line is None:
                continue

            line: list = line.split(" ")

            if line[0] == "GOTOIF" and len(line) >= 4:
                try:
                    self.create_pointer(index, self.labels[line[1]])
                except KeyError:
                    pass

                try:
                    self.create_pointer(index, self.labels[line[2]])
                except KeyError:
                    pass

            elif line[0] == "GOTO" and len(line) == 2:
                try:
                    self.create_pointer(index, self.labels[line[1]])
                except KeyError:
                    pass

            else:
                pass

        return True

    def get_result(self) -> list:
        for i in range(len(self.matrix[0])):
            if any([row[-1] for row in self.matrix]) is False:
                [row.pop() for row in self.matrix]
            else:
                break
        else:
            pass

        for index, row in enumerate(self.matrix):
            row_printable: str = ""

            for column in row[::-1]:
                row_printable += column if column else " "

            yield row_printable







