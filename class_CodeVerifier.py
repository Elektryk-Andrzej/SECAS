import variables
import discord
# import re
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs.txt", filemode="w",
                        format=f"%(levelname)s | %(message)s", datefmt="%H:%M:%S", encoding="utf8")


def log_func(func):
    def wrapper(*args, **kwargs):
        if args:
            params = f"{args} {kwargs}" if kwargs else args
        elif kwargs:
            params = kwargs
        else:
            params = "None"

        try:
            logging.debug(f'Called: {func.__name__} - {params}')

            result = func(*args, **kwargs)
            return result

        except Exception:
            logging.exception(f'{func.__name__} got fucked')
    return wrapper


@log_func
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
        print(f"{self.se_variables=}")
        for role in self.role_types:
            self.se_variables.append([role.upper(), int, True])
        print(f"{self.se_variables=}")
        for room in self.room_types:
            self.se_variables.append([room.upper(), int, True])
        print(f"{self.se_variables=}")
    @log_func
    async def no_code(self):
        await self.ctx.reply("No code to check! First line is always ignored.")

    @log_func
    async def error_template(self, position, reason):
        self.line_processing_list[position] = f"▶ {self.line_processing_list[position]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        to_append = [self.line_processing_index, error_with_arrows, reason]

        self.error_reasons.append(to_append)

    @log_func
    async def invalid_min_length(self, number_missing: int):
        reason = f"Missing arguments | {number_missing}"

        missing_arguments = ""

        for _ in range(number_missing):
            missing_arguments += "___ "

        to_append = [self.line_processing_index,
                     f"{self.line_processing_str} ▶ {missing_arguments}◀", reason]

        self.error_reasons.append(to_append)

    @log_func
    async def invalid_max_length(self, past_max_length: int):
        reason = f"Unexpected arguments | {past_max_length}"

        start_index = len(self.line_processing_list) - past_max_length

        self.line_processing_list[start_index] = f"▶ {self.line_processing_list[start_index]}"
        self.line_processing_list[-1] = f"{self.line_processing_list[-1]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)

        to_append = [self.line_processing_index, error_with_arrows, reason, None]

        self.error_reasons.append(to_append)

    @log_func
    async def invalid_number(self, position: int, number_type: type):
        reason = f"Invalid {number_type} number"

        '''if math_supported:
            self.line_processing_list[position] = f"▶ {self.line_processing_list[position]}"
            self.line_processing_list[-1] = f"{self.line_processing_list[-1]} ◀"

        else:'''

        self.line_processing_list[position] = f"▶ {self.line_processing_list[position]} ◀"

        error_with_arrows = ' '.join(self.line_processing_list)
        to_append = [self.line_processing_index, error_with_arrows, reason]

        self.error_reasons.append(to_append)

    @log_func
    async def add_line_to_result(self, emoji: str = "⁉"):
        if self.line_already_added_to_result:
            return

        if emoji == "⬛":
            to_append = f"`{len(self.processed_lines) + 1}`{emoji}"
            self.processed_lines.append(to_append)

        else:
            to_append = f"`{len(self.processed_lines) + 1}`{emoji}` {self.line_processing_str} `"
            self.processed_lines.append(to_append)

        self.line_already_added_to_result = True

    @staticmethod
    @log_func
    async def create_embed(title, description, color) -> discord.Embed:
        return discord.Embed(title=title,
                             description=description,
                             color=color)

    @log_func
    async def send_result_embed(self):
        class CallSupport(discord.ui.View):
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
                await self.ctx.reply(f"{self.ctx.author.display_name} requested help\n||<@&1138508416269156402>||")

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

        await self.ctx.channel.send(embed=final_embed, view=CallSupport(ctx=self.ctx))

    @log_func
    async def action_hint(self) -> bool:
        if not await self.is_action_required_length(2, None):
            return False

        if not await self.is_float(1):
            return False

        return True

    @log_func
    async def action_hintplayer(self) -> bool:
        if not await self.is_action_required_length(3, None):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_float(2):
            return False

        return True

    @log_func
    async def action_countdown(self) -> bool:
        if not await self.is_action_required_length(3, None):
            return False
        if not await self.is_se_variable(1):
            return False

        if not await self.is_int(2):
            return False

        return True

    @log_func
    async def action_broadcastplayer(self) -> bool:
        if not await self.is_action_required_length(3, None):
            return False
        if not await self.is_se_variable(1):
            return False
        if not await self.is_float(2):
            return False

        return True

    @log_func
    async def action_broadcast(self) -> bool:
        if not await self.is_action_required_length(2, None):
            return False

        if not await self.is_float(1):
            return False

        return True

    @log_func
    async def action_clearcassie(self) -> bool:
        if not await self.is_action_required_length(0, 0):
            return False

        return True

    @log_func
    async def action_silentcassie(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_cassie(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_clearinventory(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False
        if not await self.is_se_variable(1):
            return False

        return True

    @log_func
    async def action_removeitem(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False
        if not await self.is_se_variable(1):
            return False
        if not await self.is_variable(2, var_type=self.item_types):
            return False
        if not await self.is_int(3, required=False):
            return False

        return True

    @log_func
    async def action_give(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False
        if not await self.is_se_variable(1):
            return False
        if not await self.is_variable(2, var_type=self.item_types):
            return False
        if not await self.is_int(3, required=False):
            return False

        return True

    @log_func
    async def action_lightcolor(self) -> bool:
        if not await self.is_action_required_length(4, 4):
            return False
        if not await self.is_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        for index in range(2, 5):
            if not await self.is_int(index, min_value=0, max_value=255):
                return False

        return True

    @log_func
    async def action_resetlightcolor(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False
        if not await self.is_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        return True

    @log_func
    async def action_lightsoff(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False
        if not await self.is_variable(1, var_type=self.room_types, star_allowed=True):
            return False
        if not await self.is_float(2):
            return False

        return True

    @log_func
    async def action_goto(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False
        if not await self.is_label(1):
            return False

        return True

    @log_func
    async def action_gotoif(self) -> bool:
        if not await self.is_action_required_length(3, None):
            return False
        if not await self.is_label(1):
            return False
        if not await self.is_label(2):
            return False

        return True

    @log_func
    async def action_if(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_stop(self) -> bool:
        if not await self.is_action_required_length(0, 0):
            return False

        return True

    @log_func
    async def action_stopif(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_door(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        modes = ("LOCK", "UNLOCK", "OPEN", "CLOSE", "DESTROY")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "LOCK/UNLOCK/OPEN/CLOSE/DESTROY")
            return False

        if not await self.is_variable(2, var_type=self.door_types, star_allowed=True):
            return False

        return True

    @log_func
    async def action_tesla(self) -> bool:
        mode_selected = self.line_processing_list[1]

        if mode_selected == "ENABLE" or mode_selected == "DISABLE":
            if not await self.is_action_required_length(1, 1):
                return False

        elif mode_selected == "ROLETYPE":
            if not await self.is_action_required_length(2, 2):
                return False
            if not await self.is_variable(2, var_type=self.role_types):
                return False

        elif mode_selected == "PLAYERS":
            if not await self.is_action_required_length(2, 2):
                return False
            if not await self.is_se_variable(1):
                return False

        else:
            await self.error_template(1, "Invalid mode | "
                                         "PLAYERS/ROLETYPE/DISABLE/ENABLE")
            return False
        return True

    @log_func
    async def action_warhead(self) -> bool:
        modes = ("START", "STOP", "LOCK", "UNLOCK", "DETONATE", "BLASTDOORS")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_length(1, 1):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "START/STOP/LOCK/UNLOCK/DETONATE/BLASTDOORS")
            return False

        return True

    @log_func
    async def action_executescript(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        return True

    @log_func
    async def action_help(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_command(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_log(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_custominfo(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_length(1, None):
            return False

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                      "SET/CLEAR")
            return False
        if not await self.is_se_variable(2):
            return False

        return True

    @log_func
    async def action_damage(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False
        if not await self.is_se_variable(1):
            return False
        if not await self.is_float(2, required=False):
            return False

        return True

    @log_func
    async def action_effectperm(self) -> bool:
        modes = ("SET", "CLEAR")
        mode_selected = self.line_processing_list[1]

        if not await self.is_action_required_length(3, 4):
            return False
        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False
        if not await self.is_se_variable(1):
            return False
        if not await self.is_variable(3, var_type=self.effect_types):
            return False
        if not await self.is_float(4, required=False):
            return False

        return True

    @log_func
    async def action_radiorange(self) -> bool:
        if not await self.is_action_required_length(3, 3):
            return False

        modes = ("SET", "LOCK")
        mode_selected = self.line_processing_list[1]
        ranges = ("Short", "Medium", "Long", "Ultra")
        range_selected = self.line_processing_list[3]
        if mode_selected in modes:
            await self.error_template(1, "Invalid mode | "
                                         "SET/LOCK")
            return False
        if not await self.is_se_variable(1):
            return False

        if range_selected not in ranges:
            await self.error_template(3, "Invalid range | "
                                         "Short/Medium/Long/Ultra")
            return False

        return True

    @log_func
    async def action_kill(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        if not await self.is_se_variable(1):
            return False

        return True

    @log_func
    async def action_ahp(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not self.is_float(2):
            return False

        return True

    @log_func
    async def action_maxhp(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_float(2):
            return False

        return True

    @log_func
    async def action_hp(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_float(2):
            return False

        return True

    @log_func
    async def action_tpdoor(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(2, var_type=self.door_types):
            return False

        return True

    @log_func
    async def action_tproom(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(2, var_type=self.room_types):
            return False

        return True

    @log_func
    async def action_tpx(self) -> bool:
        if not await self.is_action_required_length(4, 4):
            return False

        if not await self.is_se_variable(1):
            return False

        for i in range(2, 5):
            if not await self.is_float(i):
                return False

        return True

    @log_func
    async def action_size(self) -> bool:
        if not await self.is_action_required_length(4, 5):
            return False

        if not await self.is_se_variable(1):
            return False

        for i in range(2, 5):
            if not await self.is_float(i):
                return False

        if not await self.is_int(5, required=False):
            return False

        return True

    @log_func
    async def action_effect(self) -> bool:
        if not await self.is_action_required_length(3, 5):
            return False

        modes = ("GIVE", "REMOVE")
        mode_selected = self.line_processing_list[1]

        if mode_selected not in modes:
            await self.error_template(1, "Invalid mode | "
                                         "GIVE/REMOVE")
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(3, var_type=self.effect_types):
            return False

        if not await self.is_int(4, required=False, min_value=0, max_value=255):
            return False

        if not await self.is_int(5, required=False):
            return False

        return True

    @log_func
    async def action_setrole(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(2, var_type=self.role_types):
            return False

        if not await self.is_int(3, required=False):
            return False

        return True

    @log_func
    async def action_advsetrole(self) -> bool:
        if not await self.is_action_required_length(2, 5):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(2, var_type=self.role_types):
            return False

        if not await self.is_bool(3, required=False):
            return False

        if not await self.is_bool(4, required=False):
            return False

        if not await self.is_int(5, required=False):
            return False

        return True

    @log_func
    async def action_ticket(self) -> bool:
        if not await self.is_action_required_length(3, 3):
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

        if not await self.is_int(3):
            return False

        return True

    @log_func
    async def action_start(self) -> bool:
        if not await self.is_action_required_length(min_len=0, max_len=0):
            return False

        return True

    @log_func
    async def action_decontaminate(self) -> bool:
        if not await self.is_action_required_length(0, 1):
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

    @log_func
    async def action_roundlock(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False
        if not await self.is_bool(1):
            return False

        return True

    @log_func
    async def action_enable(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    @log_func
    async def action_disable(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        mode_selected = self.line_processing_list[1]

        if mode_selected not in self.enable_disable_keys:
            await self.error_template(1, "Invalid key")
            return False

        return True

    @log_func
    async def action_infectrule(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False
        if not await self.is_variable(1, var_type=self.role_types, star_allowed=True):
            return False
        if not await self.is_variable(2, var_type=self.role_types):
            return False
        if not await self.is_bool(3, required=False):
            return False

        return True

    @log_func
    async def action_spawnrule(self) -> bool:
        if not await self.is_action_required_length(1, 2):
            return False
        if not await self.is_variable(1, var_type=self.role_types):
            return False
        if not await self.is_int(2, required=False):
            return False

        return True

    @log_func
    async def action_delvariable(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        if self.line_processing_list[1] not in self.se_variables:
            await self.error_template(1, "Invalid variable | "
                                         "Variable doesn't exist")
            return False

        return True

    @log_func
    async def action_delplayervariable(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        if self.line_processing_list[1] not in self.se_variables:
            await self.error_template(1, "Invalid player variable | "
                                         "Variable doesn't exist")
            return False

        return True

    @log_func
    async def action_saveplayers(self) -> bool:
        if not await self.is_action_required_length(2, 3):
            return False

        if not await self.register_variable(1, 2, player_var=True):
            return False

        if not await self.is_se_variable(2):
            return False

        if not await self.is_int(3, required=False):
            return False

        return True

    @log_func
    async def action_save(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False
        if not await self.register_variable(1, 2,
                                            everything_in_range=True, player_var=False):
            return False

        return True

    @log_func
    async def action_waitsec(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False
        if not await self.is_float(1, math_supported=True):
            return False

        return True

    @log_func
    async def action_waituntil(self) -> bool:
        if not await self.is_action_required_length(1, None):
            return False

        return True

    @log_func
    async def action_advahp(self) -> bool:
        if not await self.is_action_required_length(2, 7):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_float(2):
            return False

        if not await self.is_float(3, required=False):
            return False

        if not await self.is_float(4, required=False):
            return False

        if not await self.is_float(5, required=False):
            return False

        if not await self.is_float(6, required=False):
            return False

        if not await self.is_bool(7, required=False):
            return False

        return True

    @log_func
    async def action_reskin(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        if not await self.is_se_variable(1):
            return False

        if not await self.is_variable(2, var_type=self.role_types):
            return False

        return True

    @log_func
    async def action_httpget(self) -> bool:
        if not await self.is_action_required_length(1, 1):
            return False

        return True

    @log_func
    async def action_httppost(self) -> bool:
        if not await self.is_action_required_length(2, 2):
            return False

        return True

    @log_func
    async def register_variable(self, name_index: int, value_index: int, *,
                                player_var: bool, everything_in_range: bool = False):

        variable_name = self.line_processing_list[name_index]
        variable_value = ""

        if everything_in_range:
            variable_value = " ".join(self.line_processing_list[value_index:])
        else:
            variable_value = self.line_processing_list[value_index]

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

    @log_func
    async def is_variable(self,
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

    @log_func
    async def is_se_variable(self, line_index, *, required: bool = True) -> bool:

        if not await self.is_variable_present(line_index) and not required:
            return True

        if not await self.is_containing_brackets(line_index):
            return False

        variable = self.line_processing_list[line_index]

        if ":" in variable:
            await self.add_line_to_result("🔳")
            return True

        if await self.is_variable_provided_defined():
            return False

        return True


    @log_func
    async def is_bool(self, position, *, required: bool = True) -> bool:

        variable = self.line_processing_list[position]

        if not required:
            if len(self.line_processing_list) - 1 < position:
                return True

        if variable == "TRUE" or variable == "FALSE":
            return True

        for se_var in self.se_variables:
            if variable.replace("{", "").replace("}", "") == se_var[0] and se_var[1] is bool:
                return True

        await self.error_template(position, "Invalid TRUE/FALSE argument")
        return False

    @log_func
    async def is_label(self, position) -> bool:
        try:
            iterator = self.line_processing_list[position]

            if iterator in self.labels:
                return True
            elif int(iterator):
                reason = f"Detected line number | USE LABELS!!1!!11!"

                await self.error_template(position, reason)
                return False

        except:
            pass

        reason = f"Invalid label | Redirecting to nowhere"

        await self.error_template(position, reason)
        return False

    @log_func
    async def is_containing_brackets(self, line_index: int) -> bool:
        variable = self.line_processing_list[line_index]
        if variable[0] == "{" and variable[-1] == "}":
            return True

        await self.error_template(line_index, "No brackets provided")
        return False

    @log_func
    async def is_float(self, line_index: int, *, math_supported: bool = False,
                       required: bool = True, min_value: int = float('-inf'), max_value: int = float('inf')) -> bool:

        if not required and not await self.is_variable_present(line_index):
            return True

        if await self.is_variable_provided_defined(float, line_index):
            return True

        if not await self.is_variable_specified_type(float, line_index):
            return False

        to_be_float = self.line_processing_list[line_index]

        if not min_value <= int(eval(to_be_float)) <= max_value:
            await self.invalid_number(line_index, float)
            return False

        return True

    @log_func
    async def is_variable_present(self, line_index: int) -> bool:
        if len(self.line_processing_list) - 1 >= line_index:
            return True

    @log_func
    async def is_variable_provided_defined(self, *, var_type: type, line_index: int, player_var: bool) -> bool:

        @log_func
        async def check_in_lists(var_list: list, var_type: type, line_index: int):
            var_name = self.line_processing_list[line_index]

            for se_var in var_list:
                if var_name == se_var[0] and se_var[1] == var_type:
                    return True

                elif len(se_var) > 3 and var_name == se_var[0]:
                    try:
                        var_type(se_var[3])
                        return True
                    except:
                        pass


        if len(self.custom_variables) > 0:
            if await check_in_lists(self.custom_variables, var_type, line_index):
                return True

        elif await check_in_lists(self.se_variables, var_type, line_index):
            return True

        return False

    @log_func
    async def is_variable_specified_type(self, var_type: type, line_index: int):
        variable = self.line_processing_list[line_index]

        try:
            var_type(variable)
        except:
            await self.invalid_number(line_index, int)
            return False

        return True

    @log_func
    async def is_int(self, line_index: int, *, math_supported: bool = False, required: bool = True,
                     min_value: int = float('-inf'), max_value: int = float('inf')) -> bool:

        if (not required) and (not await self.is_variable_present(line_index)):
            return True

        if await self.is_variable_provided_defined(int, line_index):
            return True

        if not await self.is_variable_specified_type(int, line_index):
            return False

        to_be_int = self.line_processing_list[line_index]

        if not min_value <= int(eval(to_be_int)) <= max_value:
            await self.invalid_number(line_index, int)
            return False

        return True

    @log_func
    async def is_valid_condition(self, start_line_index: int):
        pass

    @log_func
    async def is_action_required_length(self, min_len: int, max_len) -> bool:
        if not min_len <= len(self.line_processing_list) - 1:
            await self.invalid_min_length(abs(len(self.line_processing_list) - 1 - min_len))

            return False

        if max_len is not None:
            if not len(self.line_processing_list) - 1 <= max_len:
                await self.invalid_max_length(len(self.line_processing_list) - 1 - max_len)

                return False

        return True
