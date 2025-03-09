from __future__ import annotations
import math
from random import randint
from enum import Enum, auto


class DNDEnum(Enum):
    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @classmethod
    def from_name(cls, name: str) -> DNDEnum:
        for e in cls:
            if name.lower() == e.name.lower():
                return e
        raise ValueError(f"Invalid {cls.__name__}: {name}")

    @classmethod
    def from_display_name(cls, name: str) -> DNDEnum:
        for e in cls:
            if e.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return e
        raise ValueError(f"Invalid {cls.__name__}: {name}")

    @classmethod
    def from_partial_name(cls, name: str) -> DNDEnum:
        for e in cls:
            if (
                "_".join([c for c in name.split(" ")])
                .lower()
                .startswith(e.name.lower())
            ):
                return e
        raise ValueError(f"Invalid partial {cls.__name__}: {name}")

    @classmethod
    def is_valid_display_name(cls, name: str) -> bool:
        return "_".join([c for c in name.split(" ")]).lower() in [
            e.name.lower() for e in cls
        ]


class Habitat(DNDEnum):
    ANY = auto()
    UNDERDARK = auto()
    URBAN = auto()
    FOREST = auto()
    GRASSLAND = auto()
    ARCTIC = auto()
    HILL = auto()
    MOUNTAIN = auto()
    UNDERWATER = auto()
    SWAMP = auto()
    COASTAL = auto()
    DESERT = auto()
    PLANAR_ABYSS = auto()
    PLANAR_NINE_HELLS = auto()
    PLANAR_UPPER_PLANES = auto()
    PLANAR_LOWER_PLANES = auto()
    PLANAR_OUTER_PLANES = auto()
    PLANAR_LIMBO = auto()
    PLANAR_FEYWILD = auto()
    PLANAR_ASTRAL_PLANE = auto()
    PLANAR_ELEMENTAL_CHAOS = auto()
    PLANAR_ELEMENTAL_PLANE_OF_FIRE = auto()
    PLANAR_ELEMENTAL_PLANE_OF_AIR = auto()
    PLANAR_ELEMENTAL_PLANE_OF_WATER = auto()
    PLANAR_ELEMENTAL_PLANE_OF_EARTH = auto()


class Treasure(DNDEnum):
    NONE = auto()
    ANY = auto()
    ARCANA = auto()
    ARMAMENTS = auto()
    IMPLEMENTS = auto()
    INDIVIDUAL = auto()
    RELICS = auto()


class Ability(DNDEnum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()

    @property
    def abbreviation(self) -> str:
        return self.name.upper()[:3]

    @staticmethod
    def from_abbreviation(abbreviation: str) -> Ability:
        for a in Ability:
            if abbreviation.upper() == a.abbreviation:
                return a
        raise ValueError(f"Invalid Ability abbreviation: {abbreviation}")


class ActionType(DNDEnum):
    ACTION = auto()
    BONUS_ACTION = auto()
    REACTION = auto()
    LEGENDARY_ACTION = auto()


class ActionSubtype(DNDEnum):
    MELEE_ATTACK_ROLL = auto()
    RANGED_ATTACK_ROLL = auto()
    MELEE_OR_RANGED_ATTACK_ROLL = auto()
    STRENGTH_SAVING_THROW = auto()
    DEXTERITY_SAVING_THROW = auto()
    CONSTITUTION_SAVING_THROW = auto()
    INTELLIGENCE_SAVING_THROW = auto()
    WISDOM_SAVING_THROW = auto()
    CHARISMA_SAVING_THROW = auto()


class Alignment(DNDEnum):
    UNALIGNED = auto()
    LAWFUL_GOOD = auto()
    NEUTRAL_GOOD = auto()
    CHAOTIC_GOOD = auto()
    LAWFUL_NEUTRAL = auto()
    NEUTRAL = auto()
    CHAOTIC_NEUTRAL = auto()
    LAWFUL_EVIL = auto()
    NEUTRAL_EVIL = auto()
    CHAOTIC_EVIL = auto()


class Condition(DNDEnum):
    BLINDED = auto()
    CHARMED = auto()
    DEAFENED = auto()
    EXHAUSTION = auto()
    FRIGHTENED = auto()
    GRAPPLED = auto()
    INCAPACITATED = auto()
    INVISIBLE = auto()
    PARALYZED = auto()
    PETRIFIED = auto()
    POISONED = auto()
    PRONE = auto()
    RESTRAINED = auto()
    STUNNED = auto()
    UNCONSCIOUS = auto()


class CreatureType(DNDEnum):
    ABERRATION = auto()
    BEAST = auto()
    CELESTIAL = auto()
    CONSTRUCT = auto()
    DRAGON = auto()
    ELEMENTAL = auto()
    FEY = auto()
    FIEND = auto()
    GIANT = auto()
    HUMANOID = auto()
    MONSTROSITY = auto()
    OOZE = auto()
    PLANT = auto()
    UNDEAD = auto()


class CoverType(DNDEnum):
    HALF_COVER = auto()
    THREE_QUARTERS_COVER = auto()
    FULL_COVER = auto()


class DamageArea(DNDEnum):
    CONE = auto()
    SPHERE = auto()
    LINE = auto()
    EMANATION = auto()


class DamageType(DNDEnum):
    ACID = auto()
    COLD = auto()
    FIRE = auto()
    FORCE = auto()
    LIGHTNING = auto()
    NECROTIC = auto()
    POISON = auto()
    PSYCHIC = auto()
    RADIANT = auto()
    THUNDER = auto()
    BLUDGEONING = auto()
    SLASHING = auto()
    PIERCING = auto()


class RollType(Enum):
    NORMAL = auto()
    AVERAGE = auto()
    MIN = auto()
    MAX = auto()


class Die(DNDEnum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20

    @property
    def avg_value(self) -> float:
        return float((self.value + 1) / 2)

    @property
    def max_value(self) -> int:
        return self.value

    @property
    def min_value(self) -> int:
        return 1

    def roll(self, num_dice: int, roll_type: RollType = RollType.NORMAL) -> int:
        match roll_type:
            case RollType.NORMAL:
                return sum(
                    [randint(self.min_value, self.max_value) for _ in range(num_dice)]
                )
            case RollType.MIN:
                return sum([self.min_value for _ in range(num_dice)])
            case RollType.MAX:
                return sum([self.max_value for _ in range(num_dice)])
            case RollType.AVERAGE:
                return math.floor(self.avg_value * num_dice)
            case _:
                raise NotImplementedError


class Hazard(DNDEnum):
    BURNING = auto()
    DEHYDRATION = auto()
    FALLING = auto()
    MALNUTRITION = auto()
    SUFFOCATION = auto()


class LanguageProficiency(DNDEnum):
    UNDERSTANDS = auto()
    SPEAKS = auto()


class Language(DNDEnum):
    COMMON = auto()
    DWARVISH = auto()
    ELVISH = auto()
    GIANT = auto()
    GNOMISH = auto()
    GOBLIN = auto()
    HALFLING = auto()
    ORC = auto()
    DRACONIC = auto()
    COMMON_SIGN_LANGUAGE = auto()
    ABYSSAL = auto()
    CELESTIAL = auto()
    INFERNAL = auto()
    DEEP_SPEECH = auto()
    PRIMORDIAL = auto()
    SYLVAN = auto()
    UNDERCOMMON = auto()

    @property
    def is_rare(self) -> bool:
        match self:
            case Language.ABYSSAL | Language.CELESTIAL | Language.INFERNAL | Language.DEEP_SPEECH | Language.PRIMORDIAL | Language.SYLVAN | Language.UNDERCOMMON:
                return True
            case _:
                return False

    @property
    def plus_amt(self) -> int:
        match self:
            case Language.COMMON:
                return 5
            case _:
                return 0

    def display_name_plus_x(self, x: int) -> str:
        if x > 5 or x < 1:
            raise ValueError
        num_words_dict = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
        return f"{self.display_name} plus {num_words_dict[x]} other language{'s' if x > 1 else ''}"

    @classmethod
    def from_display_name(cls, name: str) -> Language:
        if "plus" in name.lower():
            return next(
                (x for x in cls if f"{x.display_name.lower()} plus" in name.lower())
            )
        for x in cls:
            if x.name.lower() == "_".join([token for token in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid {cls.__name__}: {name}")


class LightingCondition(DNDEnum):
    BRIGHT_LIGHT = auto()
    DIM_LIGHT = auto()
    DARKNESS = auto()


class LimitedUsageType:
    UNLIMITED = auto()
    X_PER_DAY = auto()
    RECHARGE_X_Y = auto()
    RECHARGE_AFTER_SHORT_REST = auto()
    RECHARGE_AFTER_LONG_REST = auto()
    RECHARGE_AFTER_SHORT_OR_LONG_REST = auto()


class ObscurityLevel(DNDEnum):
    LIGHTLY_OBSCURED = auto()
    HEAVILY_OBSCURED = auto()


class Proficiency(DNDEnum):
    NORMAL = auto()
    PROFICIENT = auto()
    EXPERTISE = auto()


class Resistance(DNDEnum):
    NORMAL = auto()
    VULNERABLE = auto()
    RESISTANT = auto()
    IMMUNE = auto()


class Sense(DNDEnum):
    BLINDSIGHT = auto()
    DARKVISION = auto()
    TREMORSENSE = auto()
    TRUESIGHT = auto()


class Size(DNDEnum):
    TINY = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    HUGE = auto()
    GARGANTUAN = auto()

    @property
    def hit_die(self) -> Die:
        match self:
            case Size.TINY:
                return Die.D4
            case Size.SMALL:
                return Die.D6
            case Size.MEDIUM:
                return Die.D8
            case Size.LARGE:
                return Die.D10
            case Size.HUGE:
                return Die.D12
            case Size.GARGANTUAN:
                return Die.D20
            case _:
                raise NotImplementedError


class Skill(DNDEnum):
    # Strength
    ATHLETICS = auto()

    # Dexterity
    ACROBATICS = auto()
    SLEIGHT_OF_HAND = auto()
    STEALTH = auto()

    # Intelligence
    ARCANA = auto()
    HISTORY = auto()
    INVESTIGATION = auto()
    NATURE = auto()
    RELIGION = auto()

    # Wisdom
    ANIMAL_HANDLING = auto()
    INSIGHT = auto()
    MEDICINE = auto()
    PERCEPTION = auto()
    SURVIVAL = auto()

    # Charisma
    DECEPTION = auto()
    INTIMIDATION = auto()
    PERFORMANCE = auto()
    PERSUASION = auto()

    @property
    def associated_ability(self) -> Ability:
        match self:
            case Skill.ATHLETICS:
                return Ability.STRENGTH
            case Skill.ACROBATICS | Skill.SLEIGHT_OF_HAND | Skill.STEALTH:
                return Ability.DEXTERITY
            case Skill.ARCANA | Skill.HISTORY | Skill.INVESTIGATION | Skill.NATURE | Skill.RELIGION:
                return Ability.INTELLIGENCE
            case Skill.ANIMAL_HANDLING | Skill.INSIGHT | Skill.MEDICINE | Skill.PERCEPTION | Skill.SURVIVAL:
                return Ability.WISDOM
            case Skill.DECEPTION | Skill.INTIMIDATION | Skill.PERFORMANCE | Skill.PERSUASION:
                return Ability.CHARISMA
            case _:
                raise NotImplementedError


class SpeedType(DNDEnum):
    WALKING = auto()
    BURROW = auto()
    CLIMB = auto()
    FLY = auto()
    SWIM = auto()
