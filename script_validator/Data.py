class Data:
    class LineVerdict:
        ERRORED = "ERRORED"
        PASSED = "PASSED"
        COMMENT = "COMMENT"
        LABEL = "LABEL"
        FLAG = "FLAG"
        EMPTY = "EMPTY"
        NOT_CHECKABLE = "NOT CHECKABLE"
        TYPO = "TYPO"

    class DisableKey:
        keys: tuple = (
            "DROPPING",
            "DYING",
            "ESCAPING",
            "ELEVATORS",
            "GENERATORS",
            "HAZARDS",
            "HURTING",
            "ITEMPICKUPS",
            "LOCKERS",
            "MICROPIKUPS",
            "NTFANNOUNCEMENT",
            "PEDESTALS",
            "RESPAWNS",
            "SCP330",
            "SCP914",
            "SHOOTING",
            "TESLAS",
            "WARHEAD",
            "WORKSTATIONS"
        )

    def __init__(self):
        self.code: list or str = []
        self.code_index: int = 0
        self.line: tuple = ()
        self.processed_lines: list = []
        self.line_to_copy_for_verdict_processing: list = []
        self.show_overview: bool = False
        self.line_verdict_set: bool = False
        self.labels: list = ["NEXT", "START", "STOP"]
        self.andrzej_ping: str = "<@762016625096261652>"
        self.log_file_name: str = ""
        self.log_depth: int = 0
        self.log_depth_char: str = ">"

        self.log_handler_object = None
        self.action_handler_object = None
        self.io_handler_object = None
        self.param_handler_object = None
        self.utils_object = None
        self.verdict_handler_object = None
