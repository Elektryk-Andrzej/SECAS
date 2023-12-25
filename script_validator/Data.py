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

    class Team:
        teams: tuple = (
            "Dead",
            "SCPs",
            "ClassD",
            "FoundationForces",
            "Scientists",
            "ChaosInsurgency",
            "OtherAlive"
        )

    class Room:
        rooms: tuple = (
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
        )

    class Item:
        items: tuple = (
            "KeycardJanitor",
            "KeycardScientist",
            "KeycardResearchCoordinator",
            "KeycardZoneManager",
            "KeycardGuard",
            "KeycardNTFOfficer",
            "KeycardContainmentEngineer",
            "KeycardNTFLieutenant",
            "KeycardNTFCommander",
            "KeycardFacilityManager",
            "KeycardChaosInsurgency",
            "KeycardO5",
            "Radio",
            "GunCOM15",
            "Medkit",
            "Flashlight",
            "MicroHID",
            "SCP500",
            "SCP207",
            "Ammo12gauge",
            "GunE11SR",
            "GunCrossvec",
            "Ammo556x45",
            "GunFSP9",
            "GunLogicer",
            "GrenadeHE",
            "GrenadeFlash",
            "Ammo44cal",
            "Ammo762x39",
            "Ammo9x19",
            "GunCOM18",
            "SCP018",
            "SCP268",
            "Adrenaline",
            "Painkillers",
            "Coin",
            "ArmorLight",
            "ArmorCombat",
            "ArmorHeavy",
            "GunRevolver",
            "GunAK",
            "GunShotgun",
            "SCP330",
            "SCP2176",
            "SCP244a",
            "SCP244b",
            "SCP1853",
            "ParticleDisruptor",
            "GunCom45",
            "SCP1576",
            "Jailbird",
            "Coal",

        )

    class Effect:
        effects: tuple = (
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
        )

    class Role:
        roles: tuple = (
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
            "ChaosMarauder",
            "Scp3114",
            "Scp2536",
            "Scp1507"
        )

    class Door:
        doors: tuple = (
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
        )

    class SpawnPosition:
        positions: tuple = (
            None,
        )

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

    class Candy:
        candies: tuple = (
            None,
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
