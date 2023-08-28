import variables
import discord
import re


class CodeVerifier:
    def __init__(self, ctx, bot, code):
        self.code = code.split("\n")
        self.bot = bot
        self.ctx = ctx
        self.branch: int = 0
        self.actions: dict = {
            "HINT": self.action_hint,
            "HINTPLAYER": self.action_hintplayer,
            "COUNTDOWN": self.action_countdown,
            "BROADCASTPLAYER": self.action_broadcastplayer,
            "BROADCAST": self.action_broadcast,
            "CLEARCASSIE": self.action_clearcassie,
            "SILENTCASSIE": self.action_silentcassie,
            "CASSIE": self.action_cassie,
            "CLEARINVENTORY": self.action_clearinventory,
            "REMOVEITEM": self.action_removeitem,
            "GIVE": self.action_give,
            "LIGHTCOLOR": self.action_lightcolor,
            "LIGHTSOFF": self.action_lightsoff,
            "GOTO": self.action_goto,
            "GOTOIF": self.action_gotoif,
            "IF": self.action_if,
            "STOP": self.action_stop,
            "STOPIF": self.action_stopif,
            "DOOR": self.action_door,
            "TESLA": self.action_tesla,
            "WARHEAD": self.action_warhead,
            "EXECUTESCRIPT": self.action_executescript,
            "HELP": self.action_help,
            "COMMAND": self.action_command,
            "LOG": self.action_log,
            "CUSTOMINFO": self.action_custominfo,
            "DAMAGE": self.action_damage,
            "EFFECTPERM": self.action_effectperm,
            "RADIORANGE": self.action_radiorange,
            "KILL": self.action_kill,
            "AHP": self.action_ahp,
            "MAXHP": self.action_maxhp,
            "HP": self.action_hp,
            "TPDOOR": self.action_tpdoor,
            "TPROOM": self.action_tproom,
            "TPX": self.action_tpx,
            "SIZE": self.action_size,
            "EFFECT": self.action_effect,
            "SETROLE": self.action_setrole,
            "TICKET": self.action_ticket,
            "START": self.action_start,
            "DECONTAMINATE": self.action_decontaminate,
            "ROUNDLOCK": self.action_roundlock,
            "ENABLE": self.action_enable,
            "DISABLE": self.action_disable,
            "INFECTRULE": self.action_infectrule,
            "SPAWNRULE": self.action_spawnrule,
            "DELVARIABLE": self.action_delvariable,
            "DELPLAYERVARIABLE": self.action_delplayervariable,
            "SAVEPLAYERVARIABLE": self.action_saveplayervariable,
            "SAVEVARIABLE": self.action_savevariable,
            "WAITSEC": self.action_waitsec,
            "WAITUNTIL": self.action_waituntil,
            "RESKIN": self.action_reskin
        }
        self.line_processing_list: list = []
        self.line_processing_str: str = ""
        self.processed_lines: list = []
        self.error_reasons: list = []
        self.embed_content: str = ""
        self.errored: bool = False
        self.line_processing_index: int = 0
        self.labels = ["NEXT", "START"]
        self.line_already_added_to_result: bool = False
        self.room_types = variables.room_type
        self.item_types = variables.item_type
        self.effect_types = variables.effect_type
        self.role_types = variables.role_type
        self.door_types = variables.door_type
        self.se_variables = variables.se_variable
        self.se_player_vars = variables.se_player_variable
        self.enable_disable_keys = variables.enable_disable_key

        for role in self.role_types:
            self.se_player_vars.append(role.upper())

        for room in self.room_types:
            self.se_player_vars.append(room.upper())

    '''class ErrorMenu(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.answered = False
        @discord.ui.select(
            placeholder="Found a bug? Report it here!",
            options=[
                discord.SelectOption(label="GENERAL ERROR", value="general"),
                discord.SelectOption(label="VARIABLE ERROR", value="variable"),
                discord.SelectOption(label="LENGTH ERROR", value="length"),
                discord.SelectOption(label="ACTION ERROR", value="action"),
            ]
        )
        async def select_error(self, interaction: discord.Interaction,
                               select_item: discord.ui.Select):
            answer = select_item.values

            if not self.answered:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message("Thank you for reporting the bug")
                self.answered = True
            else:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(f"Successfully changed")'''

    @staticmethod
    async def log_to_file(text):
        with open("logs.txt", 'a') as file:
            file.write(f"{text}\n")

    async def error_template(self, position, reason, *, link):
        self.line_processing_list[position] = f"▶ {self.line_processing_list[position]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        self.error_reasons.append([self.line_processing_index, error_with_arrows, reason, link])

    async def invalid_min_length(self, number_missing: int):
        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        self.error_reasons.append([self.line_processing_index,
                                   f"{self.line_processing_str} ▶ {missing_arguments}◀", reason])

    async def invalid_max_length(self, past_max_length: int):
        reason = f"Unexpected arguments | {past_max_length}"

        start_index = len(self.line_processing_list) - past_max_length

        self.line_processing_list[start_index] = f"▶ {self.line_processing_list[start_index]}"
        self.line_processing_list[-1] = f"{self.line_processing_list[-1]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)

        self.error_reasons.append([self.line_processing_index, error_with_arrows, reason, None])

    async def invalid_number(self, position, math_supported: bool = False, number_type: str = "int"):
        reason = f"Invalid {number_type} number | M&VS - {math_supported}"
        link = "https://pastebin.com/88NLbZEw"

        if math_supported:
            self.line_processing_list[position] = f"▶ {self.line_processing_list[position]}"
            self.line_processing_list[-1] = f"{self.line_processing_list[-1]} ◀"

        else:
            self.line_processing_list[position] = f"▶ {self.line_processing_list[position]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        self.error_reasons.append([self.line_processing_index, error_with_arrows, reason, link])

    async def add_line_to_result(self, emoji: str = "⁉"):
        if self.line_already_added_to_result:
            return

        if emoji == "⬛":
            self.processed_lines.append(f"`{len(self.processed_lines) + 1}`{emoji}")

        else:
            self.processed_lines.append(f"`{len(self.processed_lines) + 1}`{emoji}"
                                        f"` {self.line_processing_str} `")

        self.line_already_added_to_result = True

    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)

    async def send_result_embed(self):
        if self.errored:
            embed_number_errors = discord.Embed(title=f"Errors found: `{len(self.error_reasons)}`",
                                                description=None,
                                                color=0xdd2e44)
            await self.ctx.channel.send(embed=embed_number_errors)

            for index, line in enumerate(self.processed_lines):
                self.embed_content += f"{line}\n"

                if len(self.embed_content) > 2000:
                    await self.ctx.channel.send(embed=await self.create_embed(
                        None, self.embed_content, 0xdd2e44))
                    self.embed_content = ""

            await self.ctx.channel.send(embed=await self.create_embed(
                None, self.embed_content, 0xdd2e44))
            self.embed_content = ""

            for line in self.error_reasons:
                if len(line) > 3 and line[3] is not None:
                    self.embed_content += f"### > [{line[2]}]({line[3]}) \n`{line[0]}`🟥` {line[1]}`\n"
                else:
                    self.embed_content += f"### > {line[2]}\n`{line[0]}`🟥` {line[1]} `\n"

                if len(self.embed_content) > 2000:
                    final_embed = discord.Embed(title=None,
                                                description=self.embed_content,
                                                color=0xdd2e44)

                    final_embed.set_footer(text=f"{self.bot.user.name} by @elektryk_andrzej",
                                           icon_url=self.bot.user.avatar)
                    await self.ctx.channel.send(embed=final_embed)

                    self.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=self.embed_content,
                                        color=0xdd2e44)

        else:
            final_embed = discord.Embed(title="No errors found!",
                                        description=self.embed_content,
                                        color=0x77b255)

        final_embed.set_footer(text=f"{self.bot.user.name} by @elektryk_andrzej",
                               icon_url=self.bot.user.avatar)

        await self.ctx.channel.send(embed=final_embed)

    async def action_hint(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_float(1):
            return False

        return True

    async def action_hintplayer(self) -> bool:
        if not await self.is_required_length(3, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars,
                                              star_allowed=True):
            return False
        if not await self.is_float(2):
            return False

        return True

    async def action_countdown(self) -> bool:
        if not await self.is_required_length(3, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars,
                                              star_allowed=True):
            return False
        if not await self.is_int(2):
            return False

        return True

    async def action_broadcastplayer(self) -> bool:
        if not await self.is_required_length(3, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars,
                                              star_allowed=True):
            return False
        if not await self.is_float(2):
            return False

        return True

    async def action_broadcast(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_float(1):
            return False

        return True

    async def action_clearcassie(self) -> bool:
        if not await self.is_required_length(0, 0):
            return False

        return True

    async def action_silentcassie(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_cassie(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_clearinventory(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False

        return True

    async def action_removeitem(self) -> bool:
        if not await self.is_required_length(2, 3):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.item_types):
            return False
        if not await self.is_int(3, math_supported=True):
            return False

        return True

    async def action_give(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.item_types):
            return False
        if not await self.is_int(3, required=False, math_supported=True):
            return False

        return True

    async def action_lightcolor(self) -> bool:
        if not await self.is_required_length(4, 4):
            return False
        if not await self.is_special_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        for index in range(2, 5):
            if not await self.is_int(index, min_value=0, max_value=255):
                return False

        return True

    async def action_resetlightcolor(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if not await self.is_special_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        return True

    async def action_lightsoff(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_special_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        if not await self.is_float(2, math_supported=True):
            return False

        return True

    async def action_goto(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if not await self.is_iterator(1):
            return False

        return True

    async def action_gotoif(self) -> bool:
        if not await self.is_required_length(3, None):
            return False
        if not await self.is_iterator(1):
            return False
        if not await self.is_iterator(2):
            return False

        return True

    async def action_if(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_stop(self) -> bool:
        if not await self.is_required_length(0, 0):
            return False

        return True

    async def action_stopif(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_door(self) -> bool:
        if not await self.is_required_length(2, None):
            return False

        modes = ("LOCK", "UNLOCK", "OPEN", "CLOSE", "DESTROY")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(2, "Invalid mode | "
                                         "LOCK/UNLOCK/OPEN/CLOSE/DESTROY", link=None)
            return False
        if not await self.is_float(3, math_supported=True, required=False):
            return False

        return True

    async def action_tesla(self) -> bool:
        mode_selected = self.line_processing_list[1]

        if mode_selected == "ENABLE" or mode_selected == "DISABLE":
            if not await self.is_required_length(1, 1):
                return False

        elif mode_selected == "ROLETYPE":
            if not await self.is_required_length(2, 2):
                return False
            if not await self.is_special_variable(2, var_type=self.role_types):
                return False

        elif mode_selected == "PLAYERS":
            if not await self.is_required_length(2, 2):
                return False
            if not await self.is_special_variable(2, var_type=self.se_player_vars, star_allowed=True):
                return False

        else:
            await self.error_template(1, "Invalid mode | "
                                         "PLAYERS/ROLETYPE/DISABLE/ENABLE", link=None)
            return False
        return True

    async def action_warhead(self) -> bool:
        modes = ("START", "STOP", "LOCK", "UNLOCK", "DETONATE", "BLASTDOORS")
        mode_selected = self.line_processing_list[1]

        if not await self.is_required_length(1, 1):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "START/STOP/LOCK/UNLOCK/DETONATE/BLASTDOORS", link=None)
            return False

        return True

    async def action_executescript(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False

        return True

    async def action_help(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_command(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_log(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_custominfo(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_required_length(1, None):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                      "SET/CLEAR", link=None)
        if not await self.is_special_variable(2, var_type=self.se_player_vars,
                                              required=False, star_allowed=True):
            return False

        return True

    async def action_damage(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_float(2, required=False):
            return False

        return True

    async def action_effectperm(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_required_length(3, 4):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE", link=None)
            return False
        if not await self.is_special_variable(2, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(3, var_type=self.effect_types):
            return False
        if not await self.is_float(4, required=False):
            return False

        return True

    async def action_radiorange(self) -> bool:
        if not await self.is_required_length(3, 3):
            return False

        modes = ("SET", "LOCK")
        mode_selected = self.line_processing_list[1]
        ranges = ("Short", "Medium", "Long", "Ultra")
        range_selected = self.line_processing_list[3]
        if mode_selected in modes:
            await self.error_template(1, "Invalid mode | "
                                         "SET/LOCK", link=None)
            return False
        if not await self.is_special_variable(2, var_type=self.se_player_vars, star_allowed=True):
            return False
        if range_selected not in ranges:
            await self.error_template(3, "Invalid range | "
                                         "Short/Medium/Long/Ultra", link=None)
            return False

        return True

    async def action_kill(self) -> bool:
        if not await self.is_required_length(1, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False

        return True

    async def action_ahp(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not self.is_float(2, math_supported=True):
            return False

        return True

    async def action_maxhp(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_float(2, math_supported=True):
            return False

        return True

    async def action_hp(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_float(2, math_supported=True):
            return False

        return True

    async def action_tpdoor(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.door_types):
            return False

        return True

    async def action_tproom(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.room_types):
            return False

        return True

    async def action_tpx(self) -> bool:
        if not await self.is_required_length(4, 4):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False

        for i in range(2, 5):
            if not await self.is_float(i):
                return False

        return True

    async def action_size(self) -> bool:
        if not await self.is_required_length(4, 5):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False

        for i in range(2, 5):
            if not await self.is_float(i):
                return False

        if not await self.is_int(5, required=False):
            return False

        return True

    async def action_effect(self) -> bool:
        if not await self.is_required_length(3, None):
            return False

        modes = ("GIVE", "REMOVE")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE", link=None)
            return False
        if not await self.is_special_variable(2, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(3, var_type=self.effect_types):
            return False
        if not await self.is_int(4, required=False, min_value=0, max_value=255):
            return False
        if not await self.is_int(5, required=False, math_supported=True):
            return False

        return True

    async def action_setrole(self) -> bool:
        if not await self.is_required_length(2, None):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.role_types):
            return False
        if not await self.is_int(3, math_supported=True, required=False):
            return False

        return True

    async def action_ticket(self) -> bool:
        if not await self.is_required_length(3, 3):
            return False

        modes = ("ADD", "REMOVE", "SET")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "ADD/REMOVE/SET", link=None)

        teams = ("ChaosInsurgency", "NineTailedFox")
        team_selected = self.line_processing_list[2]

        if team_selected not in teams:
            await self.error_template(2, "Invalid team | "
                                         "ChaosInsurgency/NineTailedFox", link=None)

        if not await self.is_int(3):
            return False

        return True

    async def action_start(self) -> bool:
        if not await self.is_required_length(min_len=0, max_len=0):
            return False

        return True

    async def action_decontaminate(self) -> bool:
        if not await self.is_required_length(0, 1):
            return False

        if len(self.line_processing_list) - 1 == 0:
            return True

        modes = ("ENABLE", "DISABLE", "FORCE")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "ENABLE/DISABLE/FORCE", link=None)
            return False

        return True

    async def action_roundlock(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if not await self.is_bool(1):
            return False

        return True

    async def action_enable(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key | Find all here",
                                      link="https://pastebin.com/iVcr4jAC")
            return False

        return True

    async def action_disable(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key | Find all here",
                                      link="https://pastebin.com/iVcr4jAC")
            return False

        return True

    async def action_infectrule(self) -> bool:
        if not await self.is_required_length(2, 3):
            return False
        if not await self.is_special_variable(1, var_type=self.role_types, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.role_types):
            return False
        if not await self.is_bool(3, required=False):
            return False

        return True

    async def action_spawnrule(self) -> bool:
        if not await self.is_required_length(1, None):
            return False
        if not await self.is_special_variable(1, var_type=self.role_types):
            return False
        if not await self.is_int(2, required=False, math_supported=True):
            return False

        return True

    async def action_delvariable(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if self.line_processing_list[1] not in self.se_variables:
            await self.error_template(1, "Invalid variable | "
                                         "Variable doesn't exist", link=None)
            return False

        return True

    async def action_delplayervariable(self) -> bool:
        if not await self.is_required_length(1, 1):
            return False
        if self.line_processing_list[1] not in self.se_player_vars:
            await self.error_template(1, "Invalid player variable | "
                                         "Variable doesn't exist", link=None)
            return False

        return True

    async def action_saveplayervariable(self) -> bool:
        if not await self.is_required_length(1, 3):
            return False
        if not await self.is_special_variable(1, var_type=None,
                                              list_appended=self.se_player_vars):
            return False
        if not await self.is_special_variable(2, var_type=self.se_player_vars,
                                              star_allowed=True):
            return False
        if not await self.is_int(3, required=False):
            return False

        return True

    async def action_savevariable(self) -> bool:
        if not await self.is_required_length(1, None):
            return False
        if not await self.is_special_variable(1, var_type=None,
                                              list_appended=self.se_variables):
            return False

        return True

    async def action_waitsec(self) -> bool:
        if not await self.is_required_length(1, None):
            return False
        if not await self.is_float(1, math_supported=True):
            return False

        return True

    async def action_waituntil(self) -> bool:
        if not await self.is_required_length(1, None):
            return False

        return True

    async def action_reskin(self) -> bool:
        if not await self.is_required_length(2, 2):
            return False
        if not await self.is_special_variable(1, var_type=self.se_player_vars, star_allowed=True):
            return False
        if not await self.is_special_variable(2, var_type=self.role_types):
            return False

        return True

    async def is_special_variable(self, line_index, *, var_type, required: bool = True,
                                  list_appended: list = None, star_allowed: bool = False) -> bool:
        variable = self.line_processing_list[line_index]

        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        if var_type is None:
            list_appended.append(variable.replace("{", "").replace("}", ""))
            return True

        if var_type[0] == "DEBUG_ROOM_TYPE":
            reason = "Invalid room variable | Find all here"
            link = "https://pastebin.com/k38VrRin"
            brackets_required = False

        elif var_type[0] == "DEBUG_ITEM_TYPE":
            reason = "Invalid item variable | Find all here"
            link = "https://pastebin.com/68X43pJU"
            brackets_required = False

        elif var_type[0] == "DEBUG_EFFECT_TYPE":
            reason = "Invalid effect variable | Find all here"
            link = "https://pastebin.com/bmXKEjTz"
            brackets_required = False

        elif var_type[0] == "DEBUG_ROLE_TYPE":
            reason = "Invalid role variable | Find all here"
            link = "https://pastebin.com/WHe38hQj"
            brackets_required = False

        elif var_type[0] == "DEGUG_DOOR_TYPE":
            reason = "Invalid door variable | Find all here"
            link = "https://pastebin.com/Z5LJ2umC"
            brackets_required = False

        elif var_type[0] == "DEBUG_SE_VARIABLE":
            reason = "Invalid `SE` variable | Find all here"
            link = "https://pastebin.com/ktwSBjJZ"
            brackets_required = True

        elif var_type[0] == "DEBUG_SE_PLAYER_VARIABLE":
            reason = "Invalid `SE` player variable | Find all here"
            link = "https://pastebin.com/5eUbbL5L"
            brackets_required = True
        else:
            reason = "Unknown error, variable check failed"
            link = None
            brackets_required = False

        if star_allowed and variable == "*":
            return True

        if brackets_required and "{" in variable and "}" in variable:
            variable = variable.replace("{", "").replace("}", "")
        elif brackets_required:
            await self.error_template(line_index, "`{}` required", link=None)
            return False

        if variable in var_type:
            return True

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        await self.error_template(line_index, reason, link=link)
        return False

    async def is_bool(self, position, *, required: bool = True) -> bool:
        if not required:
            if len(self.line_processing_list) - 1 < position:
                return True

        if self.line_processing_list[position] == "TRUE" or \
                self.line_processing_list[position] == "FALSE":
            return True
        else:
            await self.error_template(position, "Invalid TRUE/FALSE argument", link=None)
            return False

    async def is_iterator(self, position) -> bool:
        try:
            iterator = self.line_processing_list[position]

            if iterator in self.labels:
                return True
            elif int(iterator):
                reason = f"Don't use line numbers, use labels instead!!!"
                link = "https://pastebin.com/Wj97g1JX"

                await self.error_template(position, reason, link=link)
                return False

        except:
            pass

        reason = f"Invalid label | Redirecting to nowhere"
        link = "https://pastebin.com/Wj97g1JX"

        await self.error_template(position, reason, link=link)
        return False

    async def is_valid_math_operation(self, line_index: int) -> bool:
        open_brackets = 0
        for char in self.line_processing_list[line_index:]:
            if "{" in char:
                open_brackets += 1
            if "}" in char:
                open_brackets -= 1

        if open_brackets != 0:
            await self.invalid_number(line_index, True, "float")
            return False

        return True

    async def is_float(self, line_index: int, *, math_supported: bool = False,
                       required: bool = True) -> bool:
        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        to_be_float = ""
        if math_supported:
            for index in range(len(self.line_processing_list[line_index:])):
                if not await self.is_valid_math_operation(line_index + index):
                    await self.invalid_number(line_index, math_supported, "float")
                    return False

            for value in self.line_processing_list[line_index:]:
                to_be_float += re.sub(r"{.*?}", "0", value)
        else:
            to_be_float = self.line_processing_list[line_index]

        try:
            float(eval(to_be_float))
        except:
            await self.invalid_number(line_index, math_supported, "float")
            return False

        return True

    async def is_int(self, line_index: int, *, math_supported: bool = False, required: bool = True,
                     min_value: int = float('-inf'), max_value: int = float('inf')) -> bool:
        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        if math_supported:
            to_be_int = ""
            for index in range(len(self.line_processing_list[line_index:])):
                if not await self.is_valid_math_operation(line_index + index):
                    await self.invalid_number(line_index, math_supported, "int")

                    return False

            for value in self.line_processing_list[line_index:]:
                to_be_int += re.sub(r"{.*?}", "0", value)
        else:
            to_be_int = self.line_processing_list[line_index]

        try:
            if not min_value <= int(eval(to_be_int)) <= max_value:
                await self.invalid_number(line_index, math_supported, "int")
                return False
        except:
            await self.invalid_number(line_index, math_supported, "int")
            return False

        return True

    '''async def is_condition(self, position) -> bool:
        def get_se_variable_from_str(data) -> list:
            open_brackets = 0
            open_bracket_pos = []
            close_bracket_pos = []
            for index, char in enumerate(data):
                if "{" in char:
                    open_brackets += 1
                    if open_brackets > 1:
                        return False
                    else:
                        open_bracket_pos.append(index)
                if "}" in char:
                    open_brackets -= 1
                    if open_brackets < 0:
                        return False
                    else:
                        close_bracket_pos.append(index)

            if not open_brackets == 0:
                return False

            for index in range(0, len(open_bracket_pos)):
                se_variables = []
                se_variables.append(data[open_bracket_pos[index]:close_bracket_pos[index] + 1])

                return se_variables
                final_bool = []
                open_variables = []

                   if char == "=":
                        final_bool.append("==")
                    elif char == ""

                try:
                    result = eval(data)
                    return result
                except:
                    return False
            while True:
                input_data = input("Wprowadź dane: ")
                result = check_boolean_input(input_data)'''

    async def is_required_length(self, min_len: int, max_len) -> bool:
        if not min_len <= len(self.line_processing_list) - 1:
            await self.invalid_min_length(abs(len(self.line_processing_list) - 1 - min_len))

            return False

        if max_len is not None:
            if not len(self.line_processing_list) - 1 <= max_len:
                await self.invalid_max_length(len(self.line_processing_list) - 1 - max_len)

                return False

        return True
