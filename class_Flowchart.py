import colorsys

product = []


class Branch:
    def __init__(self, code, index, name):
        self.operations: list = []
        self.code: str = code
        self.index: int = index
        self.name: str = name
        self.ended: bool = False
        self.lines_done: int = 0
        print(f"!-- NEW BRANCH CREATED: \"{self.name}\"")

    async def execute(self) -> list:
        if len(self.code) <= self.index or self.index is None:
            self.ended = True
            return ["STOP", self.index]

        print(f"{self.code[int(self.index)]} "
              f"{' ' * (60 - len(self.code[int(self.index)]))} {self.name}")

        product.append(f"{self.code[int(self.index)]} "
                       f"{' ' * (60 - len(self.code[int(self.index)]))} {self.name}")
        line = self.code[int(self.index)].split(" ")

        self.index += 1

        match line[0]:
            case "GOTO":
                self.ended = True
                return ["GOTO", 2]
            case "GOTOIF":
                self.ended = True
                return ["GOTOIF", line[1], line[2]]
            case "IF":
                self.ended = True
                return ["IF", line[1]]
            case "STOPIF":
                self.ended = True
                return ["STOPIF", line[1]]
            case "STOP":
                self.ended = True
                return ["STOP"]


class Flowchart:
    def __init__(self, code):
        self.code: str = code
        self.branches: list = []
        self.labels = {"NEXT": None,
                       "START": None}
        self.line_code = None
        self.line_index: int = 0
        self.iterations: int = 0
        self.branch_history: list = []

    async def analyze(self):
        self.code = self.code.split("\n")
        if self.code[0].upper().startswith(".F"):
            self.code.pop(0)

        for index, line in enumerate(self.code):
            if line and ":" in line[-1] and " " not in line:
                line = line.replace(":", "")
                if line not in self.labels:
                    self.labels[line] = index

        print(f"!-- ALL LABELS RECORDED: {self.labels}")

    async def execute(self):
        branch = Branch(self.code, 0, "INIT")
        self.branches.append(branch)

        for branch in self.branches:
            self.iterations += 1
            if self.iterations == 10:
                break
            print(f"-> NOW EXECUTING: \"{branch.name}\"")

            while not branch.ended:
                print("s")
                if len(self.code) == self.line_index:
                    break

                next_action = await branch.execute()

                if not next_action or next_action[0] is None:
                    continue

                match next_action[0]:
                    case "GOTOIF":
                        trueline_branch = Branch(self.code, self.labels.get(next_action[1]),
                                                 f"{branch.name} -> IF_TRUE")
                        self.branches.append(trueline_branch)

                        falseline_branch = Branch(self.code, self.labels.get(next_action[2]),
                                                  f"{branch.name} -> IF_FALSE")
                        self.branches.append(falseline_branch)

                    case "IF":
                        true_branch = Branch(self.code, self.labels.get(next_action[1]),
                                             f"{branch.name} -> IF_TRUE")
                        self.branches.append(true_branch)

                    case "STOPIF":
                        false_branch = Branch(self.code, self.labels.get(next_action[1]),
                                              f"{branch.name} -> IF_FALSE")
                        self.branches.append(false_branch)

        connected_lines = ""
        for line in product:
            connected_lines += f"{line}\n"
        return connected_lines



