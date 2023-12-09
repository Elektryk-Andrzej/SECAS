from script_validator import Data, ParamHandler, Utils, VerdictHandler


# noinspection PyPep8Naming,SpellCheckingInspection
class ActionHandler:
    def __init__(self, data: Data.Data):
        self.data: Data.Data = data
        self.param: ParamHandler.ParamHandler = data.param_handler_object
        self.utils: Utils.Utils = data.utils_object
        self.verdict: VerdictHandler.VerdictHandler = data.verdict_handler_object

        self.actions: dict = {
            "HINTPLAYER": self.HINTPLAYER,
            "HINT": self.HINT,
            "COUNTDOWN": self.COUNTDOWN,
            "BROADCASTPLAYER": self.BROADCASTPLAYER,
            "BROADCAST": self.BROADCAST,
            "CLEARCASSIE": self.CLEARCASSIE,
            "SILENTCASSIE": self.SILENTCASSIE,
            "CASSIE": self.CASSIE,
            "DAMAGE": self.DAMAGE,
            "KILL": self.KILL,
            "ADVAHP": self.ADVAHP,
            "AHP": self.AHP,
            "MAXHP": self.MAXHP,
            "HP": self.HP,
            "GIVECANDY": self.GIVECANDY,
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
            "DECONTAMINATE": self.DECONTAMINATE,
            "DOOR": self.DOOR,
            "TESLA": self.TESLA,
            "WARHEAD": self.WARHEAD,
            "HTTPPOST": self.HTTPPOST,
            "HTTPGET": self.HTTPGET,
            "EXECUTESCRIPT": self.EXECUTESCRIPT,
            "HELP": self.HELP,
            "COMMAND": self.COMMAND,
            "LOG": self.LOG,
            "CUSTOMINFO": self.CUSTOMINFO,
            "EFFECTPERM": self.EFFECTPERM,
            "RADIORANGE": self.RADIORANGE,
            "RESKIN": self.RESKIN,
            "ADVSETROLE": self.ADVSETROLE,
            "TPDOOR": self.TPDOOR,
            "TPSPAWN": self.TPSPAWN,
            "TPROOM": self.TPROOM,
            "TPX": self.TPX,
            "SIZE": self.SIZE,
            "EFFECT": self.EFFECT,
            "SETROLE": self.SETROLE,
            "ENDROUND": self.ENDROUND,
            "TICKET": self.TICKET,
            "STARTROUND": self.STARTROUND,
            "ROUNDLOCK": self.ROUNDLOCK,
            "DAMAGERULE": self.DAMAGERULE,
            "DELINFECTRULE": self.DELINFECTRULE,
            "ENABLEPLAYER": self.ENABLEPLAYER,
            "DISABLEPLAYER": self.DISABLEPLAYER,
            "ENABLE": self.ENABLE,
            "DISABLE": self.DISABLE,
            "INFECTRULE": self.INFECTRULE,
            "SPAWNRULE": self.SPAWNRULE,
            "PLAYERVAR": self.PLAYERVAR,
            "DELVARIABLE": self.DELVARIABLE,
            "SAVE": self.SAVE,
            "WAITMIL": self.WAITMIL,
            "WAITSEC": self.WAITSEC,
            "WAITUNTIL": self.WAITUNTIL,
        }

    async def HINT(self) -> bool:
        if not await self.param.is_required_len(2, None):
            return False

        if not await self.param.is_number(1, float):
            return False

        await self.param.cant_check()

        return True

    async def HINTPLAYER(self) -> bool:
        if not await self.param.is_required_len(3, None):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, float):
            return False

        await self.param.cant_check()

        return True

    async def COUNTDOWN(self) -> bool:
        if not await self.param.is_required_len(3, None):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, int):
            return False

        return True

    async def BROADCASTPLAYER(self) -> bool:
        if not await self.param.is_required_len(3, None):
            return False

        if not await self.param.is_number(2, float):
            return False

        return True

    async def BROADCAST(self) -> bool:
        if not await self.param.is_required_len(2, None):
            return False

        if not await self.param.is_number(1, float):
            return False

        return True

    async def CLEARCASSIE(self) -> bool:
        if not await self.param.is_required_len(0, 0):
            return False

        return True

    async def SILENTCASSIE(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def CASSIE(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def GIVECANDY(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Candy):
            return False

        if not await self.param.is_number(3, int, required=False, min_value=1):
            return False

        return True

    async def CLEARINVENTORY(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        await self.param.cant_check(1)

        return True

    async def REMOVEITEM(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Item):
            return False

        if not await self.param.is_number(3, int, required=False):
            return False

        return True

    async def GIVE(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Item):
            return False

        if not await self.param.is_number(3, int, required=False):
            return False

        return True

    async def LIGHTCOLOR(self) -> bool:
        if not await self.param.is_required_len(4, 4):
            return False

        if not await self.param.is_non_se_variable(1,
                                                   var_type=self.data.Room,
                                                   other_syntax_allowed=("*", "ALL")):
            return False

        for index in range(2, 5):
            if not await self.param.is_number(index, int, min_value=0, max_value=255):
                return False

        return True

    async def RESETLIGHTCOLOR(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        if not await self.param.is_non_se_variable(1,
                                                   var_type=self.data.Room,
                                                   other_syntax_allowed=("*", "ALL")):
            return False

        return True

    async def LIGHTSOFF(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        if not await self.param.is_non_se_variable(1,
                                                   var_type=self.data.Room,
                                                   other_syntax_allowed=("*", "ALL")):
            return False

        if not await self.param.is_number(2, float):
            return False

        return True

    async def GOTO(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        if not await self.param.is_label(1):
            return False

        return True

    async def GOTOIF(self) -> bool:
        if not await self.param.is_required_len(3, None):
            return False

        if not await self.param.is_label(1):
            return False

        if not await self.param.is_label(2):
            return False

        return True

    async def IF(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def STOP(self) -> bool:
        if not await self.param.is_required_len(0, 0):
            return False

        return True

    async def STOPIF(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def DOOR(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        modes: tuple = "LOCK", "UNLOCK", "OPEN", "CLOSE", "DESTROY"
        if not await self.param.is_valid_mode(1, possible_modes=modes):
            return False

        if not await self.param.is_non_se_variable(2,
                                                   var_type=self.data.Door,
                                                   other_syntax_allowed=("*", "ALL")):
            return False

        return True

    async def TESLA(self) -> bool:
        mode_selected = str(await self.utils.get_str_from_line_index(1))
        modes: tuple = "ENABLE", "DISABLE", "ROLETYPE", "PLAYERS"

        if mode_selected == "ENABLE" or mode_selected == "DISABLE":
            if not await self.param.is_required_len(1, 1):
                return False

        elif mode_selected == "ROLETYPE":
            if not await self.param.is_required_len(2, 2):
                return False

            if not await self.param.is_non_se_variable(2, var_type=self.data.Role):
                return False

        elif mode_selected == "PLAYERS":
            if not await self.param.is_required_len(2, 2):
                return False

            await self.param.cant_check(1)

        else:
            closest_match: str = await self.utils.get_closest_match(mode_selected, modes)
            await self.verdict.error_template(1, f"Invalid mode", closest_match)
            return False

        return True

    async def WARHEAD(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        modes: tuple = "START", "STOP", "LOCK", "UNLOCK", "DETONATE", "BLASTDOORS"
        if not await self.param.is_valid_mode(1, possible_modes=modes):
            return False

        return True

    async def EXECUTESCRIPT(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        return True

    async def HELP(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def COMMAND(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def LOG(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def CUSTOMINFO(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("SET", "CLEAR")):
            return False

        await self.param.cant_check(2)

        return True

    async def DAMAGE(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, float, required=False):
            return False

        return True

    async def EFFECTPERM(self) -> bool:
        if not await self.param.is_required_len(3, 4):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("GIVE", "REMOVE")):
            return False

        await self.param.cant_check(2)

        if not await self.param.is_non_se_variable(3, var_type=self.data.Effect):
            return False

        if not await self.param.is_number(4, float, required=False):
            return False

        return True

    async def RADIORANGE(self) -> bool:
        if not await self.param.is_required_len(3, 3):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("SET", "LOCK")):
            return False

        await self.param.cant_check(2)

        if not await self.param.is_valid_mode(3, possible_modes=("Short", "Medium", "Long", "Ultra")):
            return False

        return True

    async def KILL(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        await self.param.cant_check(1)

        return True

    async def AHP(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not self.param.is_number(2, float):
            return False

        return True

    async def MAXHP(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, float):
            return False

        return True

    async def HP(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, float):
            return False

        return True

    async def TPDOOR(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data):
            return False

        return True

    async def TPSPAWN(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.SpawnPosition):
            return False

        return True

    async def TPROOM(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data):
            return False

        return True

    async def TPX(self) -> bool:
        if not await self.param.is_required_len(4, 4):
            return False

        await self.param.cant_check(1)

        for index in range(2, 5):
            if not await self.param.is_number(index, float):
                return False

        return True

    async def SIZE(self) -> bool:
        if not await self.param.is_required_len(4, 5):
            return False

        await self.param.cant_check(1)

        for i in range(2, 5):
            if not await self.param.is_number(i, float):
                return False

        if not await self.param.is_number(5, int, required=False):
            return False

        return True

    async def EFFECT(self) -> bool:
        if not await self.param.is_required_len(3, 5):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("GIVE", "REMOVE")):
            return False

        await self.param.cant_check(2)

        if not await self.param.is_non_se_variable(3, var_type=self.data.Effect):
            return False

        if not await self.param.is_number(4, int, required=False, min_value=0, max_value=255):
            return False

        if not await self.param.is_number(5, int, required=False):
            return False

        return True

    async def SETROLE(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Role):
            return False

        if not await self.param.is_number(3, int, required=False):
            return False

        return True

    async def ENDROUND(self) -> bool:
        if not await self.param.is_required_len(0, 0):
            return False

        return True

    async def ADVSETROLE(self) -> bool:
        if not await self.param.is_required_len(2, 5):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Role):
            return False

        if not await self.param.is_bool(3, required=False):
            return False

        if not await self.param.is_bool(4, required=False):
            return False

        if not await self.param.is_number(5, int, required=False):
            return False

        return True

    async def TICKET(self) -> bool:
        if not await self.param.is_required_len(3, 3):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("ADD", "REMOVE", "SET")):
            return False

        if not await self.param.is_valid_mode(2, possible_modes=("ChaosInsurgency", "NineTailedFox")):
            return False

        if not await self.param.is_number(3, int):
            return False

        return True

    async def STARTROUND(self) -> bool:
        if not await self.param.is_required_len(0, 0):
            return False

        return True

    async def DECONTAMINATE(self) -> bool:
        if not await self.param.is_required_len(0, 1):
            return False

        if not await self.param.is_valid_mode(1,
                                              possible_modes=("ENABLE", "DISABLE", "FORCE"),
                                              required=False):
            return False

        return True

    async def ROUNDLOCK(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        if not await self.param.is_bool(1):
            return False

        return True

    async def DAMAGERULE(self) -> bool:
        if not await self.param.is_required_len(3, 3):
            return False

        await self.param.cant_check(1)

        await self.param.cant_check(2)

        if not await self.param.is_number(3, float):
            return False

        return True

    async def DELINFECTRULE(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(2)

        return True

    async def ENABLEPLAYER(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.DisableKey.keys):
            return False

        return True

    async def DISABLEPLAYER(self) -> bool:
        return await self.ENABLEPLAYER()

    async def ENABLE(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=self.data.DisableKey.keys):
            return False

        return True

    async def DISABLE(self) -> bool:
        return await self.ENABLE()

    async def INFECTRULE(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        if not await self.param.is_non_se_variable(1,
                                                   var_type=self.data.Role,
                                                   other_syntax_allowed=("*", "ALL")):
            return False

        if not await self.param.is_non_se_variable(2, var_type=self.data.Role):
            return False

        if not await self.param.is_bool(3, required=False):
            return False

        return True

    async def SPAWNRULE(self) -> bool:
        if not await self.param.is_required_len(1, 2):
            return False

        if not await self.param.is_non_se_variable(1, var_type=self.data.Role):
            return False

        if not await self.param.is_number(2, int, required=False):
            return False

        return True

    async def DELVARIABLE(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        await self.param.cant_check(1)

        return True

    async def DELPLAYERVARIABLE(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        await self.param.cant_check(1)

        return True

    async def PLAYERVAR(self) -> bool:
        if not await self.param.is_required_len(2, 3):
            return False

        if not await self.param.is_valid_mode(1, possible_modes=("SAVE", "DELETE", "ADD", "REMOVE")):
            return False

        await self.param.cant_check(2)

        await self.param.cant_check(3)

        return True

    async def SAVE(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        await self.param.cant_check()

        return True

    async def WAITSEC(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        if not await self.param.is_number(1, float, math_supported=True):
            return False

        await self.param.cant_check()

        return True

    async def WAITMIL(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        if not await self.param.is_number(1, float, math_supported=True):
            return False

        await self.param.cant_check()

        return True

    async def WAITUNTIL(self) -> bool:
        if not await self.param.is_required_len(1, None):
            return False

        return True

    async def ADVAHP(self) -> bool:
        if not await self.param.is_required_len(2, 7):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_number(2, float):
            return False

        if not await self.param.is_number(3, float, required=False):
            return False

        if not await self.param.is_number(4, float, required=False):
            return False

        if not await self.param.is_number(5, float, required=False):
            return False

        if not await self.param.is_number(6, float, required=False):
            return False

        if not await self.param.is_bool(7, required=False):
            return False

        return True

    async def RESKIN(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check(1)

        if not await self.param.is_non_se_variable(2, var_type=self.data.Role):
            return False

        return True

    async def HTTPGET(self) -> bool:
        if not await self.param.is_required_len(1, 1):
            return False

        await self.param.cant_check()

        return True

    async def HTTPPOST(self) -> bool:
        if not await self.param.is_required_len(2, 2):
            return False

        await self.param.cant_check()

        return True
