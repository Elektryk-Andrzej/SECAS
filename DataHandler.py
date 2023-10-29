class Data:
    class LineVerdictType:
        def __init__(self):
            self.ERRORED = "line errored"
            self.PASSED = "line passed"
            self.COMMENT = "line is a comment"
            self.LABEL = "line is a label"
            self.FLAG = "line is a flag"

    class RoomType:
        def __init__(self):
            self.room_types: list[str] = [
                "LczArmory",
                "LczCurve",
                "LczStraight",
                "Lcz330",
                "Lcz914",
                "LczCrossing",
                "LczTCross",
                "LczCafe",
                "LczPlants",
                "LczToilets",
                "LczAirlock",
                "Lcz173",
                "LczClassDSpawn",
                "LczCheckpointB",
                "LczGlassBox",
                "LczCheckpointA",
                "Hcz079",
                "HczEzCheckpointA",
                "HczEzCheckpointB",
                "HczArmory",
                "Hcz939",
                "HczHid",
                "Hcz049",
                "HczChkpA",
                "HczCrossing",
                "Hcz106",
                "HczNuke",
                "HczTesla",
                "HczServers",
                "HczChkpB",
                "HczTCross",
                "HczCurve",
                "Hcz096",
                "EzVent",
                "EzIntercom",
                "EzGateA",
                "EzDownstairsPcs",
                "EzCurve",
                "EzPcs",
                "EzCrossing",
                "EzCollapsedTunnel",
                "EzConference",
                "EzStraight",
                "EzCafeteria",
                "EzUpstairsPcs",
                "EzGateB",
                "EzShelter",
                "Pocket",
                "Surface",
                "EzCheckpointHallway",
                "HczTestRoom",
                "HczStraight",
            ]

    class ItemType:
        def __init__(self):
            self.item_types: list[str] = [
                "KeycardJanitor", "0",
                "KeycardScientist", "1",
                "KeycardResearchCoordinator", "2",
                "KeycardZoneManager", "3",
                "KeycardGuard", "4",
                "KeycardNTFOfficer", "5",
                "KeycardContainmentEngineer", "6",
                "KeycardNTFLieutenant", "7",
                "KeycardNTFCommander", "8",
                "KeycardFacilityManager", "9",
                "KeycardChaosInsurgency", "10",
                "KeycardO5", "11",
                "Radio", "12",
                "GunCOM15", "13",
                "Medkit", "14",
                "Flashlight", "15",
                "MicroHID", "16",
                "SCP500", "17",
                "SCP207", "18",
                "Ammo12gauge", "19",
                "GunE11SR", "20",
                "GunCrossvec", "21",
                "Ammo556x45", "22",
                "GunFSP9", "23",
                "GunLogicer", "24",
                "GrenadeHE", "25",
                "GrenadeFlash", "26",
                "Ammo44cal", "27",
                "Ammo762x39", "28",
                "Ammo9x19", "29",
                "GunCOM18", "30",
                "SCP018", "31",
                "SCP268", "32",
                "Adrenaline", "33",
                "Painkillers", "34",
                "Coin", "35",
                "ArmorLight", "36",
                "ArmorCombat", "37",
                "ArmorHeavy", "38",
                "GunRevolver", "39",
                "GunAK", "40",
                "GunShotgun", "41",
                "SCP330", "42",
                "SCP2176", "43",
                "SCP244a", "44",
                "SCP244b", "45",
                "SCP1853", "46",
                "ParticleDisruptor", "47",
                "GunCom45", "48",
                "SCP1576", "49",
                "Jailbird", "50",
            ]

    class EffectType:
        def __init__(self):
            self.effect_types: list[str] = [
                "AmnesiaItems",
                "AmnesiaVision",
                "Asphyxiated",
                "Bleeding",
                "Blinded",
                "Burned",
                "Concussed",
                "Corroding",
                "Deafened",
                "Decontaminating",
                "Disabled",
                "Ensnared",
                "Exhausted",
                "Flashed",
                "Hemorrhage",
                "Invigorated",
                "BodyshotReduction",
                "Poisoned",
                "Scp207",
                "Invisible",
                "SinkHole",
                "DamageReduction",
                "MovementBoost",
                "RainbowTaste",
                "SeveredHands",
                "Stained",
                "Vitality",
                "Hypothermia",
                "Scp1853",
                "CardiacArrest",
                "InsufficientLighting",
                "SoundtrackMute",
                "AntiScp207",
                "Scanned"
            ]

    class RoleType:
        def __init__(self):
            self.role_types: list[str] = [
                "None",
                "Spectator",
                "CustomRole",
                "Overwatch",
                "Filmmaker",
                "Tutorial",
                "Scp173",
                "Scp106",
                "Scp049",
                "Scp0492",
                "Scp079",
                "Scp096",
                "Scp939",
                "ClassD",
                "Scientist",
                "FacilityGuard",
                "NtfPrivate",
                "NtfSergeant",
                "NtfSpecialist",
                "NtfCaptain",
                "ChaosConscript",
                "ChaosRifleman",
                "ChaosRepressor",
                "ChaosMarauder"
            ]

    class DoorType:
        def __init__(self):
            self.door_types: list[str] = [
                "Scp914Door",
                "GR18Inner",
                "Scp049Gate",
                "Scp049Armory",
                "Scp079First",
                "Scp079Second",
                "Scp096",
                "Scp106Primary",
                "Scp106Secondary",
                "Scp173Gate",
                "Scp173Connector",
                "Scp173Armory",
                "Scp173Bottom",
                "GR18Gate",
                "Scp914Gate",
                "Scp939Cryo",
                "CheckpointLczA",
                "CheckpointLczB",
                "EntranceDoor",
                "EscapePrimary",
                "EscapeSecondary",
                "ServersBottom",
                "GateA",
                "GateB",
                "HczArmory",
                "HeavyContainmentDoor",
                "HID",
                "HIDLeft",
                "HIDRight",
                "Intercom",
                "LczArmory",
                "LczCafe",
                "LczWc",
                "LightContainmentDoor",
                "NukeArmory",
                "NukeSurface",
                "PrisonDoor",
                "SurfaceGate",
                "Scp330",
                "Scp330Chamber",
                "CheckpointGate",
                "SurfaceDoor",
                "CheckpointEzHczA",
                "CheckpointEzHczB",
                "UnknownGate",
                "UnknownElevator",
                "ElevatorGateA",
                "ElevatorGateB",
                "ElevatorNuke",
                "ElevatorScp049",
                "ElevatorLczA",
                "ElevatorLczB",
                "CheckpointArmoryA",
                "CheckpointArmoryB",
                "Airlock",
                "*",
                "**",
                "!*",
                "LightContainment",
                "HeavyContainment",
                "Entrance",
                "Surface",
                "049_ARMORY",
                "079_ARMORY",
                "079_FIRST",
                "079_SECOND",
                "096",
                "106_PRIMARY",
                "106_SECONDARY",
                "173_ARMORY",
                "173_BOTTOM",
                "173_CONNECTOR",
                "173_GATE",
                "330",
                "330_CHAMBER",
                "914",
                "939_CRYO",
                "CHECKPOINT_EZ_HCZ_A",
                "CHECKPOINT_EZ_HCZ_B",
                "CHECKPOINT_LCZ_A",
                "CHECKPOINT_LCZ_B",
                "ESCAPE_PRIMARY",
                "ESCAPE_SECONDARY",
                "GATE_A",
                "GATE_B",
                "GR18",
                "GR18_INNER",
                "HCZ_ARMORY",
                "HID",
                "HID_LEFT",
                "HID_RIGHT",
                "INTERCOM",
                "LCZ_ARMORY",
                "LCZ_CAFE",
                "LCZ_WC",
                "NUKE_ARMORY",
                "SERVERS_BOTTOM",
                "SURFACE_GATE",
                "SURFACE_NUKE"
            ]

    class SEVariable:
        def __init__(self):
            self.se_variables: list[list[str, bool | None, bool]] = [
                ["DEBUG_SE_VARIABLE", None, False],
                ["CASSIESPEAKING", bool, False],
                ["DECONTAMINATED", bool, False],
                ["ISRUNNING", bool, False],
                ["ROUNDENDED", bool, False],
                ["ROUNDINPROGRESS", bool, False],
                ["ROUNDSTARTED", bool, False],
                ["SCP914ACTIVE", bool, False],
                ["WARHEADCOUNTING", bool, False],
                ["WARHEADDETONATED", bool, False],
                ["WAVERESPAWNING", bool, False],
                ["INTERCOMINUSE", bool, False],
                ["HEAVILYMODDED", bool, False],
                ["CHANCE", float, False],
                ["CHANCE10", int, False],
                ["CHANCE100", int, False],
                ["CHANCE20", int, False],
                ["CHANCE3", int, False],
                ["CHANCE5", int, False],
                ["CLASSDESCAPES", int, True],
                ["ESCAPES", int, True],
                ["SCIENTISTESCAPES", int, True],
                ["INTERCOMCOOLDOWN", float, False],
                ["INTERCOMUSETIME", float, False],
                ["DETONATIONTIME", float, False],
                ["ENGAGEDGENERATORS", int, False],
                ["PLAYERS", int, True],
                ["PLAYERSALIVE", int, True],
                ["PLAYERSDEAD", int, True],
                ["ROUNDMINUTES", float, False],
                ["ROUNDSECONDS", float, False],
                ["MAXPLAYERS", int, False],
                ["IP", str, False],
                ["PORT", str, False],
                ["DOORSTATE", str, False],
                ["LASTRESPAWNTEAM", str, False],
                ["LASTRESPAWNUNIT", str, False],
                ["NEXTWAVE", str, False],
                ["SHOW", str, False],
                ["CHAOSTICKETS", float, False],
                ["NTFTICKETS", float, False],
                ["RESPAWNEDPLAYERS", int, True],
                ["TIMESINCELASTWAVE", float, False],
                ["TIMEUNTILNEXTWAVE", float, False],
                ["TOTALWAVES", int, False],
                ["DAYOFMONTH", int, False],
                ["DAYOFWEEK", int, False],
                ["DAYOFYEAR", int, False],
                ["MONTH", int, False],
                ["TICK", int, False],
                ["YEAR", int, False],
                ["KILLS", int, False],
                ["SCPKILLS", int, False],
                ["FILTER", str, True],
                ["C", str, False],
                ["CI", int, True],
                ["GUARDS", int, True],
                ["MTFANDGUARDS", int, True],
                ["MTF", int, True],
                ["SCPS", int, True],
                ["SH", int, True],
                ["UIU", int, True],
                ["INTERCOMSPEAKER", int, True],
                ["SERVERSTAFF", int, True],
                ["EZ", int, True],
                ["HCZ", int, True],
                ["LCZ", int, True],
                ["POCKET", int, True],
                ["SURFACE", int, True],
                ["SENDER", int, True],
                ["EVPLAYER", int, True],
                ["EVATTACKER", int, True],
            ]

            self.enable_disable_key = [
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
            ]

    def __init__(self):
        self.code: list or str = []
        self.code_index: int = 0
        self.processed_lines: list = []
        self.errored: bool = False
        self.current_code_index: int = 0
        self.labels: list = ["NEXT", "START", "STOP"]
        self.custom_variables: list[list] = []
        self.andrzej_ping: str = "<@762016625096261652>"
        self.tag: str = ""
        self.log_depth: int = 1
        self.log_depth_char: str = ">"

        for role in self.RoleType().role_types:
            self.SEVariable().se_variables.append([role.upper(), int, True])
        for room in self.RoomType().room_types:
            self.SEVariable().se_variables.append([room.upper(), int, True])