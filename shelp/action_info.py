# noinspection PyPep8
BROADCAST: list = ['BROADCAST', 'Broadcasts a message to every player.', [['duration', 'float', 'true', 'The duration of the message. Variables are supported.'], ['message', 'string', 'true', 'The message. Variables are supported.']]]
# noinspection PyPep8
BROADCASTPLAYER: list = ['BROADCASTPLAYER', 'Broadcasts a message to specific player(s).', [['players', 'List<Player>', 'true', 'The players to show. Variables are supported.'], ['duration', 'float', 'true', 'The duration of the message. Variables are supported.'], ['message', 'string', 'true', 'The message. Variables are supported.']]]
# noinspection PyPep8
COUNTDOWN: list = ['COUNTDOWN', 'Displays a countdown on the player(s) screens (using broadcasts).', [['players', 'Player[]', 'true', 'The players to show the countdown to.'], ['duration', 'int', 'true', 'The duration of the countdown. Variables are supported.'], ['text', 'string', 'true', 'The text to show on the broadcast. Variables are supported.']]]
# noinspection PyPep8
HINT: list = ['HINT', 'Broadcasts a hint to every player.', [['duration', 'float', 'true', 'The duration of the message. Variables are supported.'], ['message', 'string', 'true', 'The message. Variables are supported.']]]
# noinspection PyPep8
HINTPLAYER: list = ['HINTPLAYER', 'Broadcasts a hint to specific player(s).', [['players', 'List<Player>', 'true', 'The players to show. Variables are supported.'], ['duration', 'float', 'true', 'The duration of the message. Variables are supported.'], ['message', 'string', 'true', 'The message. Variables are supported.']]]
# noinspection PyPep8
CASSIE: list = ['CASSIE', 'Makes a loud cassie announcement.', [['message', 'string', 'true', 'The message. Separate message with a | to specify a caption. Variables are supported.']]]
CLEARCASSIE: list = ['CLEARCASSIE', 'Clears cassie queue.', []]
# noinspection PyPep8
SILENTCASSIE: list = ['SILENTCASSIE', 'Makes a silent cassie announcement.', [['message', 'string', 'true', 'The message. Separate message with a | to specify a caption. Variables are supported.']]]
DEBUGCONDITIONLOG: list = ['DEBUGCONDITIONLOG', None, []]
DEBUGMATH: list = ['DEBUGMATH', None, []]
# noinspection PyPep8
ADVAHP: list = ['ADVAHP', 'Add AHP to the targeted players, with advanced settings.', [['players', 'Player[]', 'true', 'The players to affect.'], ['health', 'float', 'true', 'The amount of artificial health to add to the player.'], ['limit', 'float', 'false', 'The upper limit of AHP. Defaults to 75.'], ['decay', 'float', 'false', 'The AHP decay rate (how much AHP is lost per second). Defaults to 1.2.'], ['efficacy', 'float', 'false', 'The percent of incoming damage absorbed by AHP. Defaults to 0.7 (70%).'], ['sustain', 'float', 'false', 'The amount of time (in seconds) before the AHP begins to decay. Defaults to 0.'], ['persistent', 'bool', 'false', 'Whether or not the AHP process is removed entirely when the AHP reaches 0. Defaults to FALSE.']]]
# noinspection PyPep8
DAMAGE: list = ['DAMAGE', 'Damages the targeted player.', [['players', 'Player[]', 'true', 'The players to kill.'], ['damage', 'float', 'true', 'The amount of damage to apply. Variables are supported.'], ['damageType', 'string', 'false', 'The DeathType to apply. If a DamageType is not matched, this will act as a custom message instead. Default: Unknown']]]
# noinspection PyPep8
KILL: list = ['KILL', 'Kills the targeted players.', [['players', 'Player[]', 'true', 'The players to kill.'], ['damageType', 'DamageType', 'false', 'The ']]]
# noinspection PyPep8
AHP: list = ['AHP', 'Add AHP to the targeted players.', [['players', 'Player[]', 'true', 'The players to affect.'], ['health', 'float', 'true', 'The amount of artificial health to add to the player. Variables are supported.']]]
# noinspection PyPep8
HP: list = ['HP', 'Set the HP of the targeted players.', [['players', 'Player[]', 'true', 'The players to affect.'], ['health', 'float', 'true', 'The amount of health to set the player to. Variables are supported.']]]
# noinspection PyPep8
MAXHP: list = ['MAXHP', 'Set the Maximum HP of the targeted players.', [['players', 'Player[]', 'true', 'The players to affect.'], ['maxhealth', 'float', 'true', 'The amount of max health to set the player to. Variables ARE supported.']]]
# noinspection PyPep8
CLEARINVENTORY: list = ['CLEARINVENTORY', 'Clears inventory of the targeted players.', [['players', 'List<Player>', 'true', 'The players to remove the items from.']]]
# noinspection PyPep8
GIVE: list = ['GIVE', 'Gives the targeted players an item.', [['players', 'List<Player>', 'true', 'The players to give the item to.'], ['item', 'ItemType', 'true', 'The item to give.'], ['amount', 'int', 'false', 'The amount to give. Variables are supported. Default: 1']]]
# noinspection PyPep8
GIVECANDY: list = ['GIVECANDY', 'Gives the targeted players a candy.', [['players', 'List<Player>', 'true', 'The players to give the candy to.'], ['item', 'CandyKindID', 'true', 'The candy to give.'], ['amount', 'int', 'false', 'The amount to give. Variables are supported. Default: 1']]]
# noinspection PyPep8
REMOVEITEM: list = ['REMOVEITEM', 'Removes an item from the targeted players.', [['players', 'List<Player>', 'true', 'The players to remove the item from.'], ['item', 'ItemType', 'true', 'The item to remove.'], ['amount', 'int', 'false', 'The amount to remove. Variables are supported. Default: 1']]]
# noinspection PyPep8
LIGHTCOLOR: list = ['LIGHTCOLOR', 'Sets the lights in the provided room(s) to the given RGB color.', [['room', 'RoomType', 'true', 'The room(s) to change the color of.'], ['red', 'byte', 'true', 'The red component of the color'], ['green', 'byte', 'true', 'The green component of the color'], ['blue', 'byte', 'true', 'The blue component of the color']]]
# noinspection PyPep8
LIGHTSOFF: list = ['LIGHTSOFF', 'Turns all the lights off for a given period of time.', [['room', 'RoomType', 'true', 'The room(s) to flicker the lights off.'], ['duration', 'float', 'true', 'The duration of the lights out. Variables are supported.']]]
# noinspection PyPep8
RESETLIGHTCOLOR: list = ['RESETLIGHTCOLOR', 'Resets the light color in the given room.', [['room', 'RoomType', 'true', 'The room(s) to change the color of.']]]
# noinspection PyPep8
GOTO: list = ['GOTO', 'Moves to the provided line.', [['mode', 'string', 'false', 'The mode (ADD, do not provide for specific line)'], ['line', 'int', 'true', 'The line to move to. Variables are NOT supported.']]]
# noinspection PyPep8
GOTOIF: list = ['GOTOIF', 'Reads the condition and jumps to the first provided line if the condition is TRUE, or the second provided line if the condition is FALSE.', [['trueLine', 'string', 'true', 'The line to jump to if the condition is TRUE. Variables & Math are NOT supported.'], ['falseLine', 'string', 'true', 'The line to jump to if the condition is FALSE. Variables & Math are NOT supported.'], ['condition', 'string', 'true', 'The condition to check. Variables & Math are supported.']]]
# noinspection PyPep8
IF: list = ['IF', 'Reads the condition and stops execution of the script if the result is FALSE.', [['condition', 'string', 'true', 'The condition to check. Variables & Math are supported.']]]
STOP: list = ['STOP', 'Stops the event execution at this line.', []]
# noinspection PyPep8
STOPIF: list = ['STOPIF', 'Reads the condition and stops execution of the script if the result is TRUE.', [['condition', 'string', 'true', 'The condition to check. Variables & Math are supported.']]]
# noinspection PyPep8
DECONTAMINATE: list = ['DECONTAMINATE', 'Enables, disables, or forces decontamination.', [['mode', 'string', 'false', 'The action (ENABLE, DISABLE, FORCE). Default: FORCE']]]
# noinspection PyPep8
DOOR: list = ['DOOR', 'Controls map doors.', [['mode', 'string', 'true', 'The mode (LOCK, UNLOCK, OPEN, CLOSE, DESTROY).'], ['doors', 'List<Door>', 'true', 'The doors to affect.']]]
# noinspection PyPep8
TESLA: list = ['TESLA', 'Modifies tesla gates.', [['mode', 'string', 'true', 'The mode to run. Valid options: PLAYERS, ROLETYPE, DISABLE, ENABLE'], ['target', 'object', 'true', 'The targets. Different type based on the mode.\nPLAYERS: A list of players.\nROLETYPE: A valid RoleType (eg. ClassD, Scp173, etc)\nDISABLE & ENABLE: None'], ['duration', 'float', 'false', 'The time before reversing the effect. Variables are supported.']]]
# noinspection PyPep8
WARHEAD: list = ['WARHEAD', 'Forces a specific warhead action.', [['action', 'string', 'true', 'The action to run. Valid options: START, STOP, LOCK, UNLOCK, DETONATE, BLASTDOORS']]]
# noinspection PyPep8
COMMAND: list = ['COMMAND', 'Runs a server command with full permission.', [['command', 'string', 'true', 'The command to run.']]]
# noinspection PyPep8
EXECUTESCRIPT: list = ['EXECUTESCRIPT', 'Executes a different script.', [['scriptName', 'string', 'true', 'The name of the script.']]]
# noinspection PyPep8
HELP: list = ['HELP', 'Gets information about a command or a variable, or lists all commands or variables.', [['input', 'string', 'true', 'The name of the action/variable, \"LIST\" for all actions, or \"LISTVAR\" for all variables. Case-sensitive.']]]
# noinspection PyPep8
HTTPGET: list = ['HTTPGET', 'Sends an HTTP GET request to a website.', [['url', 'string', 'true', 'The URL to send a GET request to.']]]
# noinspection PyPep8
HTTPPOST: list = ['HTTPPOST', 'Sends an HTTP POST request to a website.', [['url', 'string', 'true', 'The URL to send a POST request to.'], ['body', 'string', 'true', 'The body to send (JSON formatting). Variables are supported.']]]
LOG: list = ['LOG', 'Creates a console log. Variables are supported.', [['message', 'string', 'true', 'The message.']]]
NULL: list = ['NULL', None, []]
# noinspection PyPep8
ADVSETROLE: list = ['ADVSETROLE', 'Sets all players to the given role with advanced settings.', [['players', 'List<Player>', 'true', 'The players to set the role as.'], ['role', 'RoleTypeId', 'true', 'The role to set all the players as.'], ['spawnpoint', 'bool', 'false', 'Use spawnpoint? default: true'], ['inventory', 'bool', 'false', 'Use default inventory? default: true'], ['max', 'int', 'false', 'The maximum amount of players to set the role of. Variables are supported. (default: unlimited).']]]
# noinspection PyPep8
CUSTOMINFO: list = ['CUSTOMINFO', 'Sets/clears the custom info of the targeted player(s).', [['mode', 'string', 'true', 'The mode (SET, CLEAR).'], ['players', 'Player[]', 'true', 'The players to affect.'], ['text', 'string', 'false', 'The text to set custom info to. Only used if mode is SET.']]]
# noinspection PyPep8
EFFECT: list = ['EFFECT', 'Action for giving/removing player effects.', [['mode', 'string', 'true', 'The mode (GIVE, REMOVE)'], ['players', 'Player[]', 'true', 'The players to affect.'], ['effect', 'EffectType', 'true', 'The effect to give or remove.'], ['intensity', 'byte', 'false', 'The intensity of the effect, between 0-255. Variables are supported. Defaults to 1.'], ['duration', 'int', 'false', 'The duration of the effect, or no duration for a permanent effect. Variables are supported.']]]
# noinspection PyPep8
EFFECTPERM: list = ['EFFECTPERM', 'Action for giving/removing permanent player effects.', [['mode', 'string', 'true', 'The mode (GIVE, REMOVE)'], ['target', 'object', 'true', 'The players to affect, or the RoleType/Team to infect with the role.'], ['effect', 'EffectType', 'true', 'The effect to give or remove.'], ['intensity', 'byte', 'false', 'The intensity of the effect, between 0-255. Variables are supported. Defaults to 1.']]]
# noinspection PyPep8
RADIORANGE: list = ['RADIORANGE', 'Modifies radio range settings.', [['mode', 'string', 'true', 'The mode to run. Valid options: SET, LOCK'], ['players', 'Player[]', 'true', 'The players to change the radio settings of.'], ['range', 'RadioRange', 'true', 'The new radio range. Must be: Short, Medium, Long, or Ultra']]]
# noinspection PyPep8
RESKIN: list = ['RESKIN', 'Sets the appearance of all players to the given role. Does NOT actually change their role -- only their appearance!', [['players', 'List<Player>', 'true', 'The players to set the role as.'], ['role', 'RoleTypeId', 'true', 'The role to set the appearance of all the players as.']]]
# noinspection PyPep8
SETROLE: list = ['SETROLE', 'Sets all players to the given role.', [['players', 'List<Player>', 'true', 'The players to set the role as.'], ['role', 'RoleTypeId', 'true', 'The role to set all the players as.'], ['max', 'int', 'false', 'The maximum amount of players to set the role of. Variables are supported. (default: unlimited).']]]
# noinspection PyPep8
SIZE: list = ['SIZE', 'Sets all players to the given size.', [['players', 'List<Player>', 'true', 'The players to rescale.'], ['size X', 'float', 'true', 'The X size to put on the player.'], ['size Y', 'float', 'true', 'The Y size to put on the player.'], ['size Z', 'float', 'true', 'The Z size to put on the player.'], ['max', 'int', 'false', 'The maximum amount of players to rescale (default: unlimited).']]]
# noinspection PyPep8
TPDOOR: list = ['TPDOOR', 'Teleports players to the specified door.', [['players', 'Player[]', 'true', 'The players to teleport'], ['door', 'DoorType', 'true', 'The door type to teleport to.']]]
# noinspection PyPep8
TPROOM: list = ['TPROOM', 'Teleports players to the specified room center.', [['players', 'Player[]', 'true', 'The players to teleport'], ['room', 'RoomType', 'true', 'The room to teleport to. Alternatively, a zone can be provided to teleport players to a random room in the zone (random for each player). Do NOT use Scp173 room!!!']]]
# noinspection PyPep8
TPSPAWN: list = ['TPSPAWN', '$"Teleports players to the specified {nameof(SpawnLocationType)}.', [['players', 'Player[]', 'true', 'The players to teleport'], ['spawn', 'SpawnLocationType', 'true', 'The spawn to teleport to.']]]
# noinspection PyPep8
TPX: list = ['TPX', 'Teleports players to the specified X, Y, Z coordinates.', [['players', 'Player[]', 'true', 'The players to teleport'], ['X', 'float', 'true', 'The X-coordinate to teleport to.'], ['Y', 'float', 'true', 'The Y-coordinate to teleport to.'], ['Z', 'float', 'true', 'The Z-coordinate to teleport to.']]]
ENDROUND: list = ['ENDROUND', 'Ends the round.', []]
# noinspection PyPep8
ROUNDLOCK: list = ['ROUNDLOCK', "Set server\'s roundlock.", [['roundlock', 'bool', 'true', 'Whether or not to lock the round.']]]
STARTROUND: list = ['STARTROUND', 'Starts the round.', []]
START: list = ['START', 'Starts the round.', []]
# noinspection PyPep8
TICKET: list = ['TICKET', 'Modifies tickets.', [['mode', 'string', 'true', 'The action (ADD, REMOVE, SET).'], ['team', 'SpawnableTeamType', 'true', 'The spawn team (ChaosInsurgency or NineTailedFox).'], ['amount', 'int', 'true', 'The amount to apply. Variables are supported.']]]
# noinspection PyPep8
DAMAGERULE: list = ['DAMAGERULE', 'Creates a new damage rule.', [['attackerRule', 'object', 'true', 'The rule for the attacker (either a role, team, or player variable)'], ['receiverRule', 'object', 'true', 'The rule for the receiver (either a role, team, or player variable)'], ['multiplier', 'float', 'true', 'The multiplier to apply to the damage rule.']]]
# noinspection PyPep8
DELINFECTRULE: list = ['DELINFECTRULE', 'Delete a currently-existing infection rule.', [['role', 'RoleTypeId', 'true', 'The role a player must die as to be infected.']]]
# noinspection PyPep8
DISABLE: list = ['DISABLE', 'Disables a feature for the entire round.', [['key', 'string', 'true', 'The key of the feature to disable. See documentation for a whole list of keys.']]]
# noinspection PyPep8
ENABLE: list = ['ENABLE', 'Enables a previously disabled round feature.', [['key', 'string', 'true', 'The key of the feature to enable. See documentation for a whole list of keys.']]]
# noinspection PyPep8
INFECTRULE: list = ['INFECTRULE', 'Creates a new infection rule.', [['oldRole', 'RoleTypeId', 'true', 'The role a player must die as to be infected.'], ['newRole', 'RoleTypeId', 'true', 'The role a player will become.'], ['movePlayer', 'bool', 'false', 'TRUE if the player should be moved to their death position, FALSE (or leave empty) to leave at spawn.']]]
# noinspection PyPep8
SPAWNRULE: list = ['SPAWNRULE', 'Creates a new spawn rule, modifying how players spawn at the start of the game. MUST BE USED BEFORE THE ROUND STARTS.', [['role', 'RoleTypeId', 'true', 'The role to create the rule for.'], ['max', 'int', 'false', 'The maximum amount of players to spawn as this role. If not provided, EVERY player who does not become a role with a different spawn rule will become this role. Variables are supported.']]]
# noinspection PyPep8
DELPLAYERVARIABLE: list = ['DELPLAYERVARIABLE', 'Deletes a previously-defined player variable.', [['variableName', 'IPlayerVariable', 'true', 'The name of the variable.']]]
# noinspection PyPep8
DELVARIABLE: list = ['DELVARIABLE', 'Deletes a previously-defined variable.', [['variableName', 'IConditionVariable', 'true', 'The name of the variable.']]]
# noinspection PyPep8
PLAYERVAR: list = ['PLAYERVAR', 'Allows manipulation of player variables.', [['mode', 'string', 'true', 'The action to perform (SAVE/DELETE/ADD/REMOVE).'], ['variableName', 'string', 'true', 'The name of the variable.'], ['players', 'Player[]', 'true', "The players. Not required if mode is \'DELETE\', but required otherwise."], ['max', 'int', 'false', "The maximum amount of players to save/add/remove. No effect if mode is \'DELETE\'. Math and variables are supported. (default: unlimited)."]]]
# noinspection PyPep8
SAVEPLAYERS: list = ['SAVEPLAYERS', 'Saves a new player variable. Saved variables can be used in ANY script, and are reset when the round ends.', [['variableName', 'string', 'true', 'The name of the new variable. Braces will be added automatically if not provided.'], ['players', 'List<Player>', 'true', 'The players to save as the new variable.'], ['max', 'int', 'false', 'The maximum amount of players to save in this variable. Math and variables are supported. (default: unlimited).']]]
# noinspection PyPep8
SAVE: list = ['SAVE', 'Saves a new variable. Saved variables can be used in ANY script, and are reset when the round ends.', [['variableName', 'string', 'true', 'The name of the new variable. Braces will be added automatically if not provided.'], ['value', 'object', 'true', 'The value to store. Variables & Math are supported.']]]
# noinspection PyPep8
WAITMIL: list = ['WAITMIL', 'Yields execution of the script for the given number of milliseconds.', [['seconds', 'float', 'true', 'The amount of milliseconds. Variables & Math are supported.']]]
# noinspection PyPep8
WAITSEC: list = ['WAITSEC', 'Yields execution of the script for the given number of seconds.', [['seconds', 'float', 'true', 'The amount of seconds. Variables & Math are supported.']]]
# noinspection PyPep8
WAITUNTIL: list = ['WAITUNTIL', 'Reads the condition and yields execution of the script until the condition is TRUE.', [['condition', 'string', 'true', 'The condition to check. Variables & Math are supported.']]]
# noinspection PyPep8
WAITUNTILDEBUG: list = ['WAITUNTILDEBUG', 'Reads the condition and yields execution of the script until the condition is TRUE.', [['condition', 'string', 'true', 'The condition to check. Variables & Math are supported.']]]
