import class_ParamHandler
param_handler = class_ParamHandler.ParamHandler()


class ActionHandler:
    def __init__(self):
        pass

    @staticmethod
    async def HINT() -> bool:
        if not await param_handler.is_action_required_len(2, None):
            return False

        if not await param_handler.is_param_number(1, float):
            return False

        return True

    async def HINTPLAYER(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def COUNTDOWN(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, int):
            return False

        return True

    async def BROADCASTPLAYER(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_number(2, float):
            return False

        return True

    async def BROADCAST(self) -> bool:
        if not await self.is_action_required_len(2, None):
            return False

        if not await self.is_param_number(1, float):
            return False

        return True

    async def CLEARCASSIE(self) -> bool:
        if not await self.is_action_required_len(0, 0):
            return False

        return True

    async def SILENTCASSIE(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def CASSIE(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def CLEARINVENTORY(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_se_var(1):
            return False

        return True

    async def REMOVEITEM(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_special_var(2, var_type=self.item_types):
            return False
        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def GIVE(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_special_var(2, var_type=self.item_types):
            return False
        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def LIGHTCOLOR(self) -> bool:
        if not await self.is_action_required_len(4, 4):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        for index in range(2, 5):
            if not await self.is_param_number(index, int, min_value=0, max_value=255):
                return False

        return True

    async def RESETLIGHTCOLOR(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        return True

    async def LIGHTSOFF(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        if not await self.is_param_number(2, float):
            return False

        return True

    async def GOTO(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_label(1):
            return False

        return True

    async def GOTOIF(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_label(1):
            return False
        if not await self.is_param_label(2):
            return False

        return True

    async def IF(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def STOP(self) -> bool:
        if not await self.is_action_required_len(0, 0):
            return False

        return True

    async def STOPIF(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def DOOR(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        modes = ("LOCK", "UNLOCK", "OPEN", "CLOSE", "DESTROY")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "LOCK/UNLOCK/OPEN/CLOSE/DESTROY")
            return False

        if not await self.is_param_special_var(2, var_type=self.door_types, star_allowed=True):
            return False

        return True

    async def TESLA(self) -> bool:
        mode_selected = self.line_processing_list[1]

        if mode_selected == "ENABLE" or mode_selected == "DISABLE":
            if not await self.is_action_required_len(1, 1):
                return False

        elif mode_selected == "ROLETYPE":
            if not await self.is_action_required_len(2, 2):
                return False
            if not await self.is_param_special_var(2, var_type=self.role_types):
                return False

        elif mode_selected == "PLAYERS":
            if not await self.is_action_required_len(2, 2):
                return False
            if not await self.is_param_se_var(1):
                return False

        else:
            await self.error_template(1, "Invalid mode | "
                                         "PLAYERS/ROLETYPE/DISABLE/ENABLE")
            return False
        return True

    async def WARHEAD(self) -> bool:
        modes = ("START", "STOP", "LOCK", "UNLOCK", "DETONATE", "BLASTDOORS")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_len(1, 1):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "START/STOP/LOCK/UNLOCK/DETONATE/BLASTDOORS")
            return False

        return True

    async def EXECUTESCRIPT(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        return True

    async def HELP(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def COMMAND(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def LOG(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def CUSTOMINFO(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_len(1, None):
            return False

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "SET/CLEAR")
            return False
        if not await self.is_param_se_var(2):
            return False

        return True

    async def DAMAGE(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_number(2, float, required=False):
            return False

        return True

    async def EFFECTPERM(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_len(3, 4):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_special_var(3, var_type=self.effect_types):
            return False
        if not await self.is_param_number(4, float, required=False):
            return False

        return True

    async def RADIORANGE(self) -> bool:
        if not await self.is_action_required_len(3, 3):
            return False

        modes = ("SET", "LOCK")
        mode_selected = self.line_processing_list[1]
        ranges = ("Short", "Medium", "Long", "Ultra")
        range_selected = self.line_processing_list[3]
        if mode_selected in modes:
            await self.error_template(1, "Invalid mode | "
                                         "SET/LOCK")
            return False
        if not await self.is_param_se_var(1):
            return False

        if range_selected not in ranges:
            await self.error_template(3, "Invalid range | "
                                         "Short/Medium/Long/Ultra")
            return False

        return True

    async def KILL(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        if not await self.is_param_se_var(1):
            return False

        return True

    async def AHP(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not self.is_param_number(2, float):
            return False

        return True

    async def MAXHP(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def HP(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def TPDOOR(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.door_types):
            return False

        return True

    async def TPROOM(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.room_types):
            return False

        return True

    async def TPX(self) -> bool:
        if not await self.is_action_required_len(4, 4):
            return False

        if not await self.is_param_se_var(1):
            return False

        for i in range(2, 5):
            if not await self.is_param_number(i, float):
                return False

        return True

    async def SIZE(self) -> bool:
        if not await self.is_action_required_len(4, 5):
            return False

        if not await self.is_param_se_var(1):
            return False

        for i in range(2, 5):
            if not await self.is_param_number(i, float):
                return False

        if not await self.is_param_number(5, int, required=False):
            return False

        return True

    async def EFFECT(self) -> bool:
        if not await self.is_action_required_len(3, 5):
            return False

        modes = ("GIVE", "REMOVE")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False

        if not await self.is_param_se_var(2):
            return False

        if not await self.is_param_special_var(3, var_type=self.effect_types):
            return False

        if not await self.is_param_number(4, int, required=False, min_value=0, max_value=255):
            return False

        if not await self.is_param_number(5, int, required=False):
            return False

        return True

    async def SETROLE(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False

        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def ADVSETROLE(self) -> bool:
        if not await self.is_action_required_len(2, 5):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False

        if not await self.is_param_bool(3, required=False):
            return False

        if not await self.is_param_bool(4, required=False):
            return False

        if not await self.is_param_number(5, int, required=False):
            return False

        return True

    async def TICKET(self) -> bool:
        if not await self.is_action_required_len(3, 3):
            return False

        modes = ("ADD", "REMOVE", "SET")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "ADD/REMOVE/SET")

        teams = ("ChaosInsurgency", "NineTailedFox")
        team_selected = self.line_processing_list[2]

        if team_selected not in teams:
            await self.error_template(2, "Invalid team | "
                                         "ChaosInsurgency/NineTailedFox")

        if not await self.is_param_number(3, int):
            return False

        return True

    async def START(self) -> bool:
        if not await self.is_action_required_len(min_len=0, max_len=0):
            return False

        return True

    async def DECONTAMINATE(self) -> bool:
        if not await self.is_action_required_len(0, 1):
            return False

        if len(self.line_processing_list) - 1 == 0:
            return True

        modes = ("ENABLE", "DISABLE", "FORCE")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "ENABLE/DISABLE/FORCE")
            return False

        return True

    async def ROUNDLOCK(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_bool(1):
            return False

        return True

    async def ENABLE(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    async def DISABLE(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    async def INFECTRULE(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_special_var(1, var_type=self.role_types, star_allowed=True):
            return False
        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False
        if not await self.is_param_bool(3, required=False):
            return False

        return True

    async def SPAWNRULE(self) -> bool:
        if not await self.is_action_required_len(1, 2):
            return False
        if not await self.is_param_special_var(1, var_type=self.role_types):
            return False
        if not await self.is_param_number(2, int, required=False):
            return False

        return True

    async def DELVARIABLE(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        variable = await self.get_str_from_line(1)
        variable = await self.strip_brackets(variable)

        try:
            if variable not in self.se_variables[0] and variable not in self.custom_variables[0]:
                await self.error_template(1, "Invalid variable | "
                                             "Variable doesn't exist")
                return False
        except:
            await self.error_template(1, "Invalid variable | "
                                         "Variable doesn't exist")
            return False

        return True

    async def DELPLAYERVARIABLE(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        variable = await self.get_str_from_line(1)
        variable = await self.strip_brackets(variable)

        if variable not in self.se_variables[0] and variable not in self.custom_variables[0]:
            await self.error_template(1, "Invalid player variable | "
                                         "Variable doesn't exist")
            return False

        return True

    async def SAVEPLAYERS(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False

        if not await self.register_variable(1, 2, player_var=True):
            return False

        if not await self.is_param_se_var(2):
            return False

        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def SAVE(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False
        if not await self.register_variable(1, 2,
                                            everything_in_range=True, player_var=False):
            return False

        return True

    async def WAITSEC(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False
        if not await self.is_param_number(1, float, math_supported=True):
            return False

        return True

    async def WAITUNTIL(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def ADVAHP(self) -> bool:
        if not await self.is_action_required_len(2, 7):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        if not await self.is_param_number(3, float, required=False):
            return False

        if not await self.is_param_number(4, float, required=False):
            return False

        if not await self.is_param_number(5, float, required=False):
            return False

        if not await self.is_param_number(6, float, required=False):
            return False

        if not await self.is_param_bool(7, required=False):
            return False

        return True

    async def RESKIN(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False

        return True

    async def HTTPGET(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        return True

    async def HTTPPOST(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        return True
