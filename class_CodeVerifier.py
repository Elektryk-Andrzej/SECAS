import variables
import discord
# import re
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs.txt", filemode="w",
                    format=f"%(levelname)s | %(message)s", datefmt="%H:%M:%S", encoding="utf8")


class CodeVerifier:
    def __init__(self, ctx, bot, code):
        self.code = code.split("\n")
        self.bot = bot
        self.ctx = ctx
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
            "RESETLIGHTCOLOR": self.action_resetlightcolor,
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
            "SAVEPLAYERS": self.action_saveplayers,
            "SAVE": self.action_save,
            "WAITSEC": self.action_waitsec,
            "WAITUNTIL": self.action_waituntil,
            "RESKIN": self.action_reskin,
            "ADVSETROLE": self.action_advsetrole,
            "ADVAHP": self.action_advahp,
            "HTTPGET": self.action_httpget,
            "HTTPPOST": self.action_httppost,
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
        self.se_variables = variables.se_variables
        self.enable_disable_keys = variables.enable_disable_key
        self.custom_variables: list[list] = []
        for role in self.role_types:
            self.se_variables.append([role.upper(), int, True])
        for room in self.room_types:
            self.se_variables.append([room.upper(), int, True])

    """
    END OF __init__ SECTION
    
    START OF ERROR HANDLING SECTION
    """

    # Simple reminidng reply
    async def error_no_code(self):
        await self.ctx.reply("No code to check! First line is always ignored.")

    # Used to handle most errors, surrounds the specified line index with arrows
    async def error_template(self, line_index, reason):
        self.line_processing_list[line_index] = f"▶ {self.line_processing_list[line_index]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        to_append = [self.line_processing_index, error_with_arrows, reason]

        self.error_reasons.append(to_append)

    # Adds three "_" for each parameter missing, while surrouding them with arrows
    async def error_invalid_min_length(self, number_missing: int):
        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        to_append = [self.line_processing_index,
                     f"{self.line_processing_str} ▶ {missing_arguments}◀", reason]

        self.error_reasons.append(to_append)

    # Surrounds all unwanted parameters with arrows
    async def error_invalid_max_length(self, past_max_length: int):
        reason = f"Unexpected arguments | {past_max_length}"

        start_index = len(self.line_processing_list) - past_max_length

        self.line_processing_list[start_index] = f"▶ {self.line_processing_list[start_index]}"
        self.line_processing_list[-1] = f"{self.line_processing_list[-1]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)

        to_append = [self.line_processing_index, error_with_arrows, reason, None]

        self.error_reasons.append(to_append)

    """
    END OF ERROR HANDLING SECTION
    
    START OF OUTPUT MANAGEMENT SECTION
    """

    # Format all of the data and add it into a list, from which it will be assembled into an embed
    async def add_line_to_result(self, emoji: str):
        if self.line_already_added_to_result:
            return

        if emoji == "⬛":
            to_append = f"`{len(self.processed_lines) + 1}`{emoji}"
            self.processed_lines.append(to_append)

        else:
            to_append = f"`{len(self.processed_lines) + 1}`{emoji}` {self.line_processing_str} `"
            self.processed_lines.append(to_append)

        self.line_already_added_to_result = True

    # Self explanatory
    @staticmethod
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)

    async def send_result_embed(self):
        """class CallSupport(discord.ui.View):
            def __init__(self, ctx):
                super().__init__()
                self.ctx = ctx

            @discord.ui.button(
                label="Having trouble? Call support!",
                style=discord.ButtonStyle.blurple
            )
            async def button_clicked(self, interaction: discord.Interaction, button: discord.Button):
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message("Message sent!", ephemeral=True)
                await self.ctx.reply(f"{interaction.user} requested help\n||<@&1138508416269156402>||")

        class CallDev(discord.ui.View):
            def __init__(self, ctx):
                super().__init__()
                self.ctx = ctx

            @discord.ui.button(
                label="Found a bug? Call devs!",
                style=discord.ButtonStyle.red
            )
            async def button_clicked(self, interaction: discord.Interaction, button: discord.Button):
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message("Message sent!", ephemeral=True)
                await self.ctx.reply(f"{interaction.user} requested help\n||<@762016625096261652>||")"""

        if self.errored:
            embed_number_errors = await self.create_embed(f"Errors found: `{len(self.error_reasons)}`",
                                                          None,
                                                          0xdd2e44)
            await self.ctx.reply(embed=embed_number_errors, mention_author=False)

            for index, line in enumerate(self.processed_lines):
                self.embed_content += f"{line}\n"

                if len(self.embed_content) > 2000:
                    await self.ctx.channel.send(embed=await self.create_embed(
                                                None,
                                                self.embed_content,
                                                0xdd2e44))
                    self.embed_content = ""

            await self.ctx.channel.send(embed=await self.create_embed(
                                        None,
                                        self.embed_content,
                                        0xdd2e44))
            self.embed_content = ""

            for line in self.error_reasons:
                self.embed_content += f"### > {line[2]}\n`{line[0]}`🟥` {line[1]} `\n"

                if len(self.embed_content) > 2000:
                    await self.ctx.channel.send(embed=await self.create_embed(
                                                None,
                                                self.embed_content,
                                                0xdd2e44))

                    self.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=self.embed_content,
                                        color=0xdd2e44)

        else:
            await self.ctx.channel.send(embed=await self.create_embed(
                                 "No errors found!",
                                 None,
                                 0x77b255),
                                 mention_author=False)

            for index, line in enumerate(self.processed_lines):
                self.embed_content += f"{line}\n"

                if len(self.embed_content) > 2000:
                    await self.ctx.channel.send(embed=await self.create_embed(
                                                None,
                                                self.embed_content,
                                                0x77b255))
                    self.embed_content = ""

            final_embed = discord.Embed(title=None,
                                        description=self.embed_content,
                                        color=0x77b255)

        final_embed.set_footer(text=f"{self.bot.user.name}by @elektryk_andrzej",
                               icon_url=self.bot.user.avatar)

        await self.ctx.channel.send(embed=final_embed, mention_author=False)

    """
    END OF OUTPUT MANAGEMENT SECTION
    
    START OF ACTION SECTION
    
    
    Basic action check schematic:
    
    > Check if param is as it should be
    > If it's good, check the next param, if not, return False
    >> Errors are usually raised in the middle of the "check tree" (things like is_action_required_len),
    >> so operating on bool values is essential to pass the info that something went wrong to lower parts
    > If all params were checked and none returned False, return True
    """

    async def action_hint(self) -> bool:
        if not await self.is_action_required_len(2, None):
            return False

        if not await self.is_param_number(1, float):
            return False

        return True

    async def action_hintplayer(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def action_countdown(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, int):
            return False

        return True

    async def action_broadcastplayer(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_number(2, float):
            return False

        return True

    async def action_broadcast(self) -> bool:
        if not await self.is_action_required_len(2, None):
            return False

        if not await self.is_param_number(1, float):
            return False

        return True

    async def action_clearcassie(self) -> bool:
        if not await self.is_action_required_len(0, 0):
            return False

        return True

    async def action_silentcassie(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_cassie(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_clearinventory(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_se_var(1):
            return False

        return True

    async def action_removeitem(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_special_var(2, var_type=self.item_types):
            return False
        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def action_give(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_special_var(2, var_type=self.item_types):
            return False
        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def action_lightcolor(self) -> bool:
        if not await self.is_action_required_len(4, 4):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        for index in range(2, 5):
            if not await self.is_param_number(index, int, min_value=0, max_value=255):
                return False

        return True

    async def action_resetlightcolor(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        return True

    async def action_lightsoff(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False
        if not await self.is_param_special_var(1, var_type=self.room_types, star_allowed=True):
            return False
        if not await self.is_param_number(2, float):
            return False

        return True

    async def action_goto(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_label(1):
            return False

        return True

    async def action_gotoif(self) -> bool:
        if not await self.is_action_required_len(3, None):
            return False
        if not await self.is_param_label(1):
            return False
        if not await self.is_param_label(2):
            return False

        return True

    async def action_if(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_stop(self) -> bool:
        if not await self.is_action_required_len(0, 0):
            return False

        return True

    async def action_stopif(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_door(self) -> bool:
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

    async def action_tesla(self) -> bool:
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

    async def action_warhead(self) -> bool:
        modes = ("START", "STOP", "LOCK", "UNLOCK", "DETONATE", "BLASTDOORS")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_len(1, 1):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "START/STOP/LOCK/UNLOCK/DETONATE/BLASTDOORS")
            return False

        return True

    async def action_executescript(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        return True

    async def action_help(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_command(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_log(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_custominfo(self) -> bool:
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

    async def action_damage(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_se_var(1):
            return False
        if not await self.is_param_number(2, float, required=False):
            return False

        return True

    async def action_effectperm(self) -> bool:
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

    async def action_radiorange(self) -> bool:
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

    async def action_kill(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        if not await self.is_param_se_var(1):
            return False

        return True

    async def action_ahp(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not self.is_param_number(2, float):
            return False

        return True

    async def action_maxhp(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def action_hp(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_number(2, float):
            return False

        return True

    async def action_tpdoor(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.door_types):
            return False

        return True

    async def action_tproom(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.room_types):
            return False

        return True

    async def action_tpx(self) -> bool:
        if not await self.is_action_required_len(4, 4):
            return False

        if not await self.is_param_se_var(1):
            return False

        for i in range(2, 5):
            if not await self.is_param_number(i, float):
                return False

        return True

    async def action_size(self) -> bool:
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

    async def action_effect(self) -> bool:
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

    async def action_setrole(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False

        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def action_advsetrole(self) -> bool:
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

    async def action_ticket(self) -> bool:
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

    async def action_start(self) -> bool:
        if not await self.is_action_required_len(min_len=0, max_len=0):
            return False

        return True

    async def action_decontaminate(self) -> bool:
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

    async def action_roundlock(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False
        if not await self.is_param_bool(1):
            return False

        return True

    async def action_enable(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    async def action_disable(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    async def action_infectrule(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False
        if not await self.is_param_special_var(1, var_type=self.role_types, star_allowed=True):
            return False
        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False
        if not await self.is_param_bool(3, required=False):
            return False

        return True

    async def action_spawnrule(self) -> bool:
        if not await self.is_action_required_len(1, 2):
            return False
        if not await self.is_param_special_var(1, var_type=self.role_types):
            return False
        if not await self.is_param_number(2, int, required=False):
            return False

        return True

    async def action_delvariable(self) -> bool:
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

    async def action_delplayervariable(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        variable = await self.get_str_from_line(1)
        variable = await self.strip_brackets(variable)

        if variable not in self.se_variables[0] and variable not in self.custom_variables[0]:
            await self.error_template(1, "Invalid player variable | "
                                         "Variable doesn't exist")
            return False

        return True

    async def action_saveplayers(self) -> bool:
        if not await self.is_action_required_len(2, 3):
            return False

        if not await self.register_variable(1, 2, player_var=True):
            return False

        if not await self.is_param_se_var(2):
            return False

        if not await self.is_param_number(3, int, required=False):
            return False

        return True

    async def action_save(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False
        if not await self.register_variable(1, 2,
                                            everything_in_range=True, player_var=False):
            return False

        return True

    async def action_waitsec(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False
        if not await self.is_param_number(1, float, math_supported=True):
            return False

        return True

    async def action_waituntil(self) -> bool:
        if not await self.is_action_required_len(1, None):
            return False

        return True

    async def action_advahp(self) -> bool:
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

    async def action_reskin(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        if not await self.is_param_se_var(1):
            return False

        if not await self.is_param_special_var(2, var_type=self.role_types):
            return False

        return True

    async def action_httpget(self) -> bool:
        if not await self.is_action_required_len(1, 1):
            return False

        return True

    async def action_httppost(self) -> bool:
        if not await self.is_action_required_len(2, 2):
            return False

        return True

    """
    END OF ACTION SECTION
    
    START OF ACTION HANDLING SECTION
    """

    # Register a certain value to a SE variable
    async def register_variable(self, name_index: int, value_index: int, *,
                                player_var: bool, everything_in_range: bool = False):

        variable_name = await self.get_str_from_line(name_index)
        variable_name = await self.strip_brackets(variable_name)
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.line_processing_list[value_index:])
        else:
            variable_value = await self.get_str_from_line(value_index)

        if not await self.is_containing_brackets(name_index):
            return False

        async def get_type() -> type or bool:
            if variable_value.lower() == "true" or variable_value.lower() == "false":
                return bool

            try:
                int(variable_value)
                return int
            except ValueError:
                pass

            try:
                float(variable_value)
                return float
            except ValueError:
                pass

            try:
                str(variable_value)
                return str
            except ValueError:
                pass

            return False

        if not player_var:
            if not await get_type():
                await self.error_template(variable_value, "Couldn't convert variable to any type")
                return None

            self.custom_variables.append([variable_name, await get_type(), False, variable_value])

        elif player_var:
            self.custom_variables.append([variable_name, int, True, variable_value])

        return True

    # Handles all non-standard variables, like doors, rooms, roles etc.
    # Requires to specify a list which is to be checked
    async def is_param_special_var(self,
                                   line_index: int, *, var_type: list,
                                   required: bool = True, star_allowed: bool = False) -> bool:
        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        variable = self.line_processing_list[line_index]

        if var_type[0] == "DEBUG_ROOM_TYPE":
            reason = "Invalid room variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_ITEM_TYPE":
            reason = "Invalid item variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_EFFECT_TYPE":
            reason = "Invalid effect variable"
            brackets_required = False

        elif var_type[0] == "DEBUG_ROLE_TYPE":
            reason = "Invalid role variable"
            brackets_required = False

        elif var_type[0] == "DEGUG_DOOR_TYPE":
            reason = "Invalid door variable"
            brackets_required = False

        else:
            reason = "UNKNOWN ERROR | CONTACT ANDRZEJ"
            brackets_required = False

        if star_allowed and variable == "*":
            return True
        elif not star_allowed and variable == "*":
            await self.error_template(line_index, "* usage forbidden | Use other values")
            return False

        if brackets_required and "{" in variable and "}" in variable:
            variable = variable.replace("{", "").replace("}", "")

        elif brackets_required:
            await self.error_template(line_index, "`{}` required")
            return False

        if variable in var_type:
            return True

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        await self.error_template(line_index, reason)
        return False

    async def is_param_se_var(self, line_index, *, required: bool = True) -> bool:
        if not await self.is_variable_present(line_index) and not required:
            return True

        if not await self.is_containing_brackets(line_index):
            return False

        variable = await self.get_str_from_line(line_index)
        variable = await self.strip_brackets(variable)

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        if await self.is_variable_defined(var_type=int,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.se_variables):
            return True

        if variable == "*":
            await self.error_template(line_index, "Asterisk usage forbidden")
            return False

        await self.error_template(line_index, "Invalid SE variable")
        return False

    async def is_param_bool(self, line_index, *, required: bool = True) -> bool:

        variable = await self.get_str_from_line(line_index)

        if not required:
            if len(self.line_processing_list) - 1 < line_index:
                return True

        if variable == "TRUE" or variable == "FALSE":
            return True

        for se_var in self.se_variables:
            if variable.replace("{", "").replace("}", "") == se_var[0] and se_var[1] is bool:
                return True

        await self.error_template(line_index, "Invalid TRUE/FALSE argument")
        return False

    async def is_param_label(self, line_index) -> bool:
        try:
            iterator = await self.get_str_from_line(line_index)

            if iterator in self.labels:
                return True
            elif int(iterator):
                await self.error_template(line_index, f"Detected number | USE LABELS!")
                return False

        except:
            await self.error_template(line_index, f"Invalid label")
            return False

    async def is_containing_brackets(self, line_index: int) -> bool:
        variable = await self.get_str_from_line(line_index)
        if not (variable[0] == "{" and variable[-1] == "}"):
            return False

        variable = variable.removeprefix("{").removesuffix("}")

        if "{" in variable or "}" in variable:
            return False

        return True

    # Check if len(list) can accommodate a param at the specified index
    async def is_variable_present(self, line_index: int) -> bool:
        if len(self.line_processing_list) - 1 >= line_index:
            return True
        else:
            return False

    # Get a value from the line list, report error if outside of range
    async def get_str_from_line(self, line_index) -> str:
        try:
            return str(self.line_processing_list[line_index]).strip()
        except IndexError:
            await self.report_bug(line_index,
                                  "Tried to get a value that's outside of the line."
                                  "Returned the last value in the line instead.")
            return str(self.line_processing_list[-1]).strip()

    # Send a message that something went wrong
    async def report_bug(self, line_index: int, error: str):
        self.ctx.reply(f"""
        The bot has experienced a bug:
        `{error}` | param `{line_index}` @ line `{self.line_processing_index}`
        """)

    @staticmethod
    async def strip_brackets(val: str) -> str:
        return val.replace("{", "").replace("}", "")

    # Check if a variable in a list is present, True if is, False if not
    async def is_variable_defined(self, *, var_type: type, line_index: int, player_var: bool, var_list: list) -> bool:
        if var_list == self.se_variables:
            var_list = self.se_variables + self.custom_variables

        var_name = await self.get_str_from_line(line_index)
        var_name = await self.strip_brackets(var_name)

        for se_var in var_list:
            print(se_var)
            # Skip check if name is not the same, or if variable is a player var or not
            if not var_name == se_var[0] or not se_var[2] == player_var:
                continue

            # Check variable type
            if se_var[1] == var_type:
                return True

            # Try to force the value into a requested one (only possible with custom variables)
            if len(se_var) > 3:
                try:
                    var_type(se_var[3])
                    return True
                except:
                    continue

        return False

    async def is_variable_specified_type(self, var_type: type, line_index: int):
        variable = await self.get_str_from_line(line_index)

        try:
            var_type(variable)
            return True
        except:
            return False

    async def is_param_number(self, line_index: int, var_type: int or float, *,
                              math_supported: bool = False,
                              required: bool = True,
                              min_value: int = float('-inf'),
                              max_value: int = float('inf')) -> bool:

        if (not required) and (not await self.is_variable_present(line_index)):
            return True

        if await self.is_variable_defined(var_type=var_type,
                                          line_index=line_index,
                                          player_var=True,
                                          var_list=self.se_variables):
            return True

        if await self.is_variable_specified_type(var_type, line_index):
            return True

        if math_supported:
            await self.add_line_to_result("🔲")
            return True

        to_be_number = await self.get_str_from_line(line_index)

        try:
            if min_value <= var_type(eval(to_be_number)) <= max_value:
                return True
        except:
            pass

        await self.error_template(line_index, "Invalid integer number")
        return False

    async def is_action_required_len(self, min_len: int, max_len) -> bool:
        if not min_len <= len(self.line_processing_list) - 1:
            await self.error_invalid_min_length(abs(len(self.line_processing_list) - 1 - min_len))

            return False

        if max_len is not None:
            if not len(self.line_processing_list) - 1 <= max_len:
                await self.error_invalid_max_length(len(self.line_processing_list) - 1 - max_len)

                return False

        return True
