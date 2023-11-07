import Data
import ParamHandler
import Utils
import VerdictHandler


# noinspection PyPep8Naming
class ActionHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data

        self.param_handler: ParamHandler.ParamHandler = ParamHandler.ParamHandler(data)

        self.utils: Utils.Utils = Utils.Utils(data)

        self.verdict_handler: VerdictHandler.VerdictHandler = VerdictHandler.VerdictHandler(data)

        self.actions: dict = {
            "HINT": self.HINT,
            "HINTPLAYER": self.HINTPLAYER,
            "COUNTDOWN": self.COUNTDOWN,
            "BROADCASTPLAYER": self.BROADCASTPLAYER,
            "BROADCAST": self.BROADCAST,
            "CLEARCASSIE": self.CLEARCASSIE,
            "SILENTCASSIE": self.SILENTCASSIE,
            "CASSIE": self.CASSIE,
            "CLEARINVENTORY": self.CLEARINVENTORY,
            "REMOVEITEM": self.REMOVEITEM,
            "GIVE": self.GIVE,
            "LIGHTCOLOR": self.LIGHTCOLOR,
            "RESETLIGHTCOLOR": self.RESETLIGHTCOLOR,
            "LIGHTSOFF": self.LIGHTSOFF,
            "GOTO": self.GOTO,
            "GOTOIF": self.GOTOIF,
            "IF": self.IF,
            "STOP": self.STOP,
            "STOPIF": self.STOPIF,
            "DOOR": self.DOOR,
            "TESLA": self.TESLA,
            "WARHEAD": self.WARHEAD,
            "EXECUTESCRIPT": self.EXECUTESCRIPT,
            "HELP": self.HELP,
            "COMMAND": self.COMMAND,
            "LOG": self.LOG,
            "CUSTOMINFO": self.CUSTOMINFO,
            "DAMAGE": self.DAMAGE,
            "EFFECTPERM": self.EFFECTPERM,
            "RADIORANGE": self.RADIORANGE,
            "KILL": self.KILL,
            "AHP": self.AHP,
            "MAXHP": self.MAXHP,
            "HP": self.HP,
            "TPDOOR": self.TPDOOR,
            "TPROOM": self.TPROOM,
            "TPX": self.TPX,
            "SIZE": self.SIZE,
            "EFFECT": self.EFFECT,
            "SETROLE": self.SETROLE,
            "TICKET": self.TICKET,
            "START": self.START,
            "DECONTAMINATE": self.DECONTAMINATE,
            "ROUNDLOCK": self.ROUNDLOCK,
            "ENABLE": self.ENABLE,
            "DISABLE": self.DISABLE,
            "INFECTRULE": self.INFECTRULE,
            "SPAWNRULE": self.SPAWNRULE,
            "DELVARIABLE": self.DELVARIABLE,
            "DELPLAYERVARIABLE": self.DELPLAYERVARIABLE,
            "SAVEPLAYERS": self.SAVEPLAYERS,
            "SAVE": self.SAVE,
            "WAITSEC": self.WAITSEC,
            "WAITUNTIL": self.WAITUNTIL,
            "RESKIN": self.RESKIN,
            "ADVSETROLE": self.ADVSETROLE,
            "ADVAHP": self.ADVAHP,
            "HTTPGET": self.HTTPGET,
            "HTTPPOST": self.HTTPPOST,
        }

    async def HINT(self) -> bool:
        if not await self.param_handler.is_required_len(2, None):
            return False

        elif not await self.param_handler.is_number(1, float):
            return False

        return True

    async def HINTPLAYER(self) -> bool:
        if not await self.param_handler.is_required_len(3, None):
            return False

        elif not await self.param_handler.is_se_var(1):
            return False

        elif not await self.param_handler.is_number(2, float):
            return False

        return True

    async def COUNTDOWN(self) -> bool:
        if not await self.param_handler.is_required_len(3, None):
            return False

        elif not await self.param_handler.is_se_var(1):
            return False

        elif not await self.param_handler.is_number(2, int):
            return False

        return True

    async def BROADCASTPLAYER(self) -> bool:
        if not await self.param_handler.is_required_len(3, None):
            return False

        elif not await self.param_handler.is_se_var(1):
            return False

        elif not await self.param_handler.is_number(2, float):
            return False

        return True

    async def BROADCAST(self) -> bool:
        if not await self.param_handler.is_required_len(2, None):
            return False

        elif not await self.param_handler.is_number(1, float):
            return False

        return True

    async def CLEARCASSIE(self) -> bool:
        if not await self.param_handler.is_required_len(0, 0):
            return False

        return True

    async def SILENTCASSIE(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def CASSIE(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def CLEARINVENTORY(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        elif not await self.param_handler.is_se_var(1):
            return False

        return True

    async def REMOVEITEM(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        elif not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.ItemType):
            return False

        if not await self.param_handler.is_number(3, int, required=False):
            return False

        return True

    async def GIVE(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.ItemType):
            return False

        if not await self.param_handler.is_number(3, int, required=False):
            return False

        return True

    async def LIGHTCOLOR(self) -> bool:
        if not await self.param_handler.is_required_len(4, 4):
            return False

        if not await self.param_handler.is_special_var(1,
                                                       var_type=self.data.RoomType,
                                                       star_allowed=True):
            return False

        for index in range(2, 5):
            if not await self.param_handler.is_number(index, int, min_value=0, max_value=255):
                return False

        return True

    async def RESETLIGHTCOLOR(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        if not await self.param_handler.is_special_var(1,
                                                       var_type=self.data.RoomType,
                                                       star_allowed=True):
            return False

        return True

    async def LIGHTSOFF(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_special_var(1,
                                                       var_type=self.data.RoomType,
                                                       star_allowed=True):
            return False

        if not await self.param_handler.is_number(2, float):
            return False

        return True

    async def GOTO(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        if not await self.param_handler.is_label(1):
            return False

        return True

    async def GOTOIF(self) -> bool:
        if not await self.param_handler.is_required_len(3, None):
            return False

        if not await self.param_handler.is_label(1):
            return False

        if not await self.param_handler.is_label(2):
            return False

        return True

    async def IF(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def STOP(self) -> bool:
        if not await self.param_handler.is_required_len(0, 0):
            return False

        return True

    async def STOPIF(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def DOOR(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        modes = ("lock", "unlock", "open", "close", "destroy")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "LOCK/UNLOCK/OPEN/CLOSE/DESTROY")
            return False

        if not await self.param_handler.is_special_var(2,
                                                       var_type=self.data.DoorType,
                                                       star_allowed=True):
            return False

        return True

    async def TESLA(self) -> bool:
        mode_selected = await self.utils.get_str_from_line_index(1)
        mode_selected = mode_selected.casefold()

        if mode_selected == "enable" or mode_selected == "disable":
            if not await self.param_handler.is_required_len(1, 1):
                return False

        elif mode_selected == "roletype":
            if not await self.param_handler.is_required_len(2, 2):
                return False

            if not await self.param_handler.is_special_var(2, var_type=self.data.RoleType):
                return False

        elif mode_selected == "players":
            if not await self.param_handler.is_required_len(2, 2):
                return False

            if not await self.param_handler.is_se_var(1):
                return False

        else:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "PLAYERS/ROLETYPE/DISABLE/ENABLE")
            return False
        return True

    async def WARHEAD(self) -> bool:
        modes = ("start", "stop", "lock", "unlock", "detonate", "blastdoors")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if not await self.param_handler.is_required_len(1, 1):
            return False

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "START/STOP/LOCK/UNLOCK/DETONATE/BLASTDOORS")
            return False

        return True

    async def EXECUTESCRIPT(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        return True

    async def HELP(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def COMMAND(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def LOG(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def CUSTOMINFO(self) -> bool:
        modes = ("set", "clear")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if not await self.param_handler.is_required_len(1, None):
            return False

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "SET/CLEAR")
            return False

        if not await self.param_handler.is_se_var(2):
            return False

        return True

    async def DAMAGE(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_number(2, float, required=False):
            return False

        return True

    async def EFFECTPERM(self) -> bool:
        modes = ("set", "clear")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if not await self.param_handler.is_required_len(3, 4):
            return False

        if mode_selected not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(3, var_type=self.data.EffectType):
            return False

        if not await self.param_handler.is_number(4, float, required=False):
            return False

        return True

    async def RADIORANGE(self) -> bool:
        if not await self.param_handler.is_required_len(3, 3):
            return False

        modes = ("set", "lock")
        mode_selected = await self.utils.get_str_from_line_index(1)
        ranges = ("short", "medium", "long", "Uultra")
        range_selected = await self.utils.get_str_from_line_index(3)

        if mode_selected.casefold() in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "SET/LOCK")
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if range_selected.casefold() not in ranges:
            await self.verdict_handler.error_template(3, "Invalid range | "
                                         "Short/Medium/Long/Ultra")
            return False

        return True

    async def KILL(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        return True

    async def AHP(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not self.param_handler.is_number(2, float):
            return False

        return True

    async def MAXHP(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_number(2, float):
            return False

        return True

    async def HP(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_number(2, float):
            return False

        return True

    async def TPDOOR(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data):
            return False

        return True

    async def TPROOM(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data):
            return False

        return True

    async def TPX(self) -> bool:
        if not await self.param_handler.is_required_len(4, 4):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        for i in range(2, 5):
            if not await self.param_handler.is_number(i, float):
                return False

        return True

    async def SIZE(self) -> bool:
        if not await self.param_handler.is_required_len(4, 5):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        for i in range(2, 5):
            if not await self.param_handler.is_number(i, float):
                return False

        if not await self.param_handler.is_number(5, int, required=False):
            return False

        return True

    async def EFFECT(self) -> bool:
        if not await self.param_handler.is_required_len(3, 5):
            return False

        modes = ("give", "remove")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False

        if not await self.param_handler.is_se_var(2):
            return False

        if not await self.param_handler.is_special_var(3, var_type=self.data.EffectType):
            return False

        if not await self.param_handler.is_number(4, int, required=False, min_value=0, max_value=255):
            return False

        if not await self.param_handler.is_number(5, int, required=False):
            return False

        return True

    async def SETROLE(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.RoleType):
            return False

        if not await self.param_handler.is_number(3, int, required=False):
            return False

        return True

    async def ADVSETROLE(self) -> bool:
        if not await self.param_handler.is_required_len(2, 5):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.RoleType):
            return False

        if not await self.param_handler.is_bool(3, required=False):
            return False

        if not await self.param_handler.is_bool(4, required=False):
            return False

        if not await self.param_handler.is_number(5, int, required=False):
            return False

        return True

    async def TICKET(self) -> bool:
        if not await self.param_handler.is_required_len(3, 3):
            return False

        modes = ("add", "remove", "set")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "ADD/REMOVE/SET")

        teams = ("ChaosInsurgency", "NineTailedFox")
        team_selected = await self.utils.get_str_from_line_index(2)

        if team_selected not in teams:
            await self.verdict_handler.error_template(2, "Invalid team | "
                                         "ChaosInsurgency/NineTailedFox")

        if not await self.param_handler.is_number(3, int):
            return False

        return True

    async def START(self) -> bool:
        if not await self.param_handler.is_required_len(0, 0):
            return False

        return True

    async def DECONTAMINATE(self) -> bool:
        if not await self.param_handler.is_required_len(0, 1):
            return False

        if len(self.data.line) - 1 == 0:
            return True

        modes = ("enable", "disable", "force")
        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected.casefold() not in modes:
            await self.verdict_handler.error_template(1, "Invalid mode | "
                                         "ENABLE/DISABLE/FORCE")
            return False

        return True

    async def ROUNDLOCK(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        if not await self.param_handler.is_bool(1):
            return False

        return True

    async def ENABLE(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected not in self.data.SEVariable.enable_disable_key:
            await self.verdict_handler.error_template(1, "Invalid key")
            return False

        return True

    async def DISABLE(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        mode_selected = await self.utils.get_str_from_line_index(1)

        if mode_selected not in self.data.SEVariable.enable_disable_key:
            await self.verdict_handler.error_template(1, "Invalid key")
            return False

        return True

    async def INFECTRULE(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        if not await self.param_handler.is_special_var(1,
                                                       var_type=self.data.RoleType,
                                                       star_allowed=True):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.RoleType):
            return False

        if not await self.param_handler.is_bool(3, required=False):
            return False

        return True

    async def SPAWNRULE(self) -> bool:
        if not await self.param_handler.is_required_len(1, 2):
            return False

        if not await self.param_handler.is_special_var(1, var_type=self.data.RoleType):
            return False

        if not await self.param_handler.is_number(2, int, required=False):
            return False

        return True

    async def DELVARIABLE(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        '''variable = await self.utils.get_str_from_line_index(1)
        variable = await self.utils.strip_brackets(variable)

        try:
            if variable in self.data.SEVariable.se_variables[0][0] or variable in self.data.custom_variables[0]:
                await self.verdict_handler.error_template(1, "Invalid variable | "
                                             "Variable doesn't exist")
                return True
        except:
            await self.verdict_handler.error_template(1, "Invalid variable | "
                                         "Variable doesn't exist")
            return False'''

        return True

    async def DELPLAYERVARIABLE(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        '''variable = await self.utils.get_str_from_line_index(1)
        variable = await self.utils.strip_brackets(variable)

        if variable not in self.data.se_variables[0] and variable not in self.data.custom_variables[0]:
            await self.verdict_handler.error_template(1, "Invalid player variable | "
                                         "Variable doesn't exist")
            return False'''

        return True

    async def SAVEPLAYERS(self) -> bool:
        if not await self.param_handler.is_required_len(2, 3):
            return False

        if not await self.param_handler.register_var(1, 2, player_var=True):
            return False

        if not await self.param_handler.is_se_var(2):
            return False

        if not await self.param_handler.is_number(3, int, required=False):
            return False

        return True

    async def SAVE(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        if not await self.param_handler.register_var(1, 2,
                                                     everything_in_range=True, player_var=False):
            return False

        return True

    async def WAITSEC(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        if not await self.param_handler.is_number(1, float, math_supported=True):
            return False

        return True

    async def WAITUNTIL(self) -> bool:
        if not await self.param_handler.is_required_len(1, None):
            return False

        return True

    async def ADVAHP(self) -> bool:
        if not await self.param_handler.is_required_len(2, 7):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_number(2, float):
            return False

        if not await self.param_handler.is_number(3, float, required=False):
            return False

        if not await self.param_handler.is_number(4, float, required=False):
            return False

        if not await self.param_handler.is_number(5, float, required=False):
            return False

        if not await self.param_handler.is_number(6, float, required=False):
            return False

        if not await self.param_handler.is_bool(7, required=False):
            return False

        return True

    async def RESKIN(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        if not await self.param_handler.is_se_var(1):
            return False

        if not await self.param_handler.is_special_var(2, var_type=self.data.RoleType):
            return False

        return True

    async def HTTPGET(self) -> bool:
        if not await self.param_handler.is_required_len(1, 1):
            return False

        return True

    async def HTTPPOST(self) -> bool:
        if not await self.param_handler.is_required_len(2, 2):
            return False

        return True
