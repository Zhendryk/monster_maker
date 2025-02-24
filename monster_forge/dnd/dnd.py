from __future__ import annotations
import math
from random import randint
from enum import Enum, auto
from dataclasses import dataclass, field
from collections.abc import Sequence
from functools import cached_property


class Sense(Enum):
    BLINDSIGHT = auto()
    DARKVISION = auto()
    TREMORSENSE = auto()
    TRUESIGHT = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Sense:
        for x in Sense:
            if x.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid Sense: {name}")


class Condition(Enum):
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

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Condition:
        for x in Condition:
            if x.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid Condition: {name}")


class DamageType(Enum):
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

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> DamageType:
        for x in DamageType:
            if x.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid DamageType: {name}")


class Resistance(Enum):
    NORMAL = auto()
    VULNERABLE = auto()
    RESISTANT = auto()
    IMMUNE = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Resistance:
        for x in Resistance:
            if x.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid Resistance: {name}")


class Proficiency(Enum):
    NORMAL = auto()
    PROFICIENT = auto()
    EXPERTISE = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Proficiency:
        for x in Proficiency:
            if x.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return x
        raise ValueError(f"invalid Proficiency: {name}")


class LanguageProficiency(Enum):
    UNDERSTANDS = auto()
    SPEAKS = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> LanguageProficiency:
        for lp in LanguageProficiency:
            if lp.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return lp
        raise ValueError(f"invalid LanguageProficiency: {name}")


class Skill(Enum):
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
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Skill:
        for s in Skill:
            if s.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return s
        raise ValueError(f"invalid Skill: {name}")

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


class SpeedType(Enum):
    WALKING = auto()
    BURROW = auto()
    CLIMB = auto()
    FLY = auto()
    SWIM = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> SpeedType:
        for s in SpeedType:
            if s.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return s
        raise ValueError(f"invalid Speed Type: {name}")


class RollType(Enum):
    NORMAL = auto()
    AVERAGE = auto()
    MIN = auto()
    MAX = auto()


class Die(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20

    @property
    def avg_value(self) -> float:
        return float(self.value + 1) / 2

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


@dataclass
class Dice:
    dice: dict[Die, int]

    @property
    def value(self) -> int:
        return sum([dt.roll(self.dice[dt]) for dt in self.dice])

    @property
    def average_value(self) -> int:
        return sum(
            [dt.roll(self.dice[dt], roll_type=RollType.AVERAGE) for dt in self.dice]
        )

    @property
    def max_value(self) -> int:
        return sum([dt.roll(self.dice[dt], roll_type=RollType.MAX) for dt in self.dice])

    @property
    def min_value(self) -> int:
        return sum([dt.roll(self.dice[dt], roll_type=RollType.MIN) for dt in self.dice])

    @property
    def range(self) -> range:
        return range(
            start=self.min_value, stop=self.max_value + 1
        )  # +1 because it is not inclusive of the upper bound

    def hit_points(self, ability_scores: AbilityScores) -> str:
        if len(self.dice) > 1:
            raise NotImplementedError
        die, cnt = self.dice.popitem()
        self.dice[die] = cnt
        total_hp = self.average_value + ability_scores.constitution_modifier * cnt
        return f"{total_hp} ({cnt}{die.name.lower()} + {ability_scores.constitution_modifier * cnt})"

    @property
    def num_hit_dice(self) -> int:
        return sum(cnt for cnt in self.dice.values())

    @staticmethod
    def closest_to(hp: int, monster_size: Size, max_range: int = 51) -> Dice:
        distances = {
            i: abs(hp - Dice({monster_size.hit_die: i}).average_value)
            for i in range(max_range)
        }
        closest = min(distances, key=lambda k: distances[k])
        return Dice({monster_size.hit_die: closest})


class Ability(Enum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_display_name(name: str) -> Ability:
        for a in Ability:
            if a.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return a
        raise ValueError(f"invalid Ability: {name}")


class Size(Enum):
    TINY = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    HUGE = auto()
    GARGANTUAN = auto()

    @staticmethod
    def from_name(size_name: str) -> Size:
        for s in Size:
            if size_name.lower() == s.name.lower():
                return s
        raise ValueError(f"Invalid size: {size_name}")

    @staticmethod
    def from_display_name(name: str) -> Size:
        for s in Size:
            if s.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return s
        raise ValueError(f"invalid Size: {name}")

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

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])


@dataclass
class AbilityScores:
    scores: dict[Ability, int]

    def _calculate_modifier(self, score: int) -> int:
        return math.floor(float((score - 10) / 2))

    @property
    def strength_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.STRENGTH])

    @property
    def dexterity_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.DEXTERITY])

    @property
    def constitution_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.CONSTITUTION])

    @property
    def intelligence_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.INTELLIGENCE])

    @property
    def wisdom_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.WISDOM])

    @property
    def charisma_modifier(self) -> int:
        return self._calculate_modifier(self.scores[Ability.CHARISMA])


class Language(Enum):
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

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

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


CR_EXPERIENCE_POINTS: dict[int | float, int] = {
    0: 10,
    1 / 8: 25,
    1 / 4: 50,
    1 / 2: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300,
    7: 2900,
    8: 3900,
    9: 5000,
    10: 5900,
    11: 7200,
    12: 8400,
    13: 10000,
    14: 11500,
    15: 13000,
    16: 15000,
    17: 18000,
    18: 20000,
    19: 22000,
    20: 25000,
    21: 33000,
    22: 41000,
    23: 50000,
    24: 62000,
    25: 75000,
    26: 90000,
    27: 105000,
    28: 120000,
    29: 135000,
    30: 155000,
}
CR_AC: dict[int | float, int] = {
    0: 10,
    1 / 8: 11,
    1 / 4: 11,
    1 / 2: 12,
    1: 12,
    2: 13,
    3: 13,
    4: 14,
    5: 15,
    6: 15,
    7: 15,
    8: 15,
    9: 16,
    10: 17,
    11: 17,
    12: 17,
    13: 18,
    14: 19,
    15: 19,
    16: 19,
    17: 20,
    18: 21,
    19: 21,
    20: 21,
    21: 22,
    22: 23,
    23: 23,
    24: 23,
    25: 24,
    26: 25,
    27: 25,
    28: 25,
    29: 26,
    30: 27,
}


@dataclass
class ChallengeRating:

    rating: int | float
    has_lair: bool = False

    @property
    def proficiency_bonus(self) -> int:
        if self.rating >= 0 and self.rating <= 4:
            return 2
        elif self.rating >= 5 and self.rating <= 8:
            return 3
        elif self.rating >= 9 and self.rating <= 12:
            return 4
        elif self.rating >= 13 and self.rating <= 16:
            return 5
        elif self.rating >= 17 and self.rating <= 20:
            return 6
        elif self.rating >= 21 and self.rating <= 24:
            return 7
        elif self.rating >= 25 and self.rating <= 28:
            return 8
        elif self.rating >= 29 and self.rating <= 30:
            return 9
        raise NotImplementedError

    @property
    def lair_rating(self) -> int | float:
        return self.rating + 1

    @property
    def experience_points(self) -> int:
        return CR_EXPERIENCE_POINTS[self.rating]

    @property
    def lair_xp(self) -> int:
        return CR_EXPERIENCE_POINTS[self.lair_rating]

    @property
    def armor_class(self) -> int:
        return CR_AC[self.rating]

    @property
    def lair_armor_class(self) -> int:
        return CR_AC[self.lair_rating]

    def hit_points(self, ability_scores: AbilityScores, monster_size: Size) -> str:
        if self.rating < 1:
            hp = math.ceil(30 * math.sqrt(self.rating))
        elif self.rating >= 1 and self.rating <= 19:
            hp = math.ceil(15 * (self.rating + 1))
        else:
            hp = math.ceil(45 * (self.rating - 13))
        hit_dice = Dice.closest_to(hp, monster_size)
        return hit_dice.hit_points(ability_scores)

    @property
    def display(self) -> str:
        if isinstance(self.rating, float):
            numerator, denominator = self.rating.as_integer_ratio()
            if denominator == 1:
                if self.has_lair:
                    return f"{numerator} (XP {self.experience_points}, or {self.lair_xp} in lair; PB +{self.proficiency_bonus})"
                return f"{numerator} (XP {self.experience_points}; PB +{self.proficiency_bonus})"
            if self.has_lair:
                return f"{numerator}/{denominator} (XP {self.experience_points}, or {self.lair_xp} in lair; PB +{self.proficiency_bonus})"
            return f"{numerator}/{denominator} (XP {self.experience_points}; PB +{self.proficiency_bonus})"
        elif self.has_lair:
            return f"{self.rating} (XP {self.experience_points}, or {self.lair_xp} in lair; PB +{self.proficiency_bonus})"
        return (
            f"{self.rating} (XP {self.experience_points}; PB +{self.proficiency_bonus})"
        )


@dataclass
class Encounter:
    size: EncounterSize | None = field(default=None)
    difficulty: EncounterDifficulty | None = field(default=None)
    num_pcs: int | None = field(default=None)
    avg_party_level: int | None = field(default=None)
    player_levels: Sequence[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        pass
        # if not self.player_levels:
        #     assert self.num_pcs is not None
        #     assert self.avg_party_level is not None
        # else:
        #     assert self.player_levels is not None

    @cached_property
    def calced_avg_party_level(self) -> int:
        if self.player_levels:
            return math.floor(sum(self.player_levels) / self.num_players)
        return self.avg_party_level

    @cached_property
    def calced_num_players(self) -> int:
        if self.player_levels:
            return len(self.player_levels)
        return self.num_pcs

    @cached_property
    def num_monsters(self) -> int:
        return self.size.num_creatures

    @cached_property
    def monster_cr(self) -> int | float:
        total_xp_budget = self.difficulty.experience_points_budget(
            self.calced_avg_party_level, num_players=self.calced_num_players
        )
        xp_per_monster = total_xp_budget / self.num_monsters
        distances = [
            (cr, abs(xp_per_monster - cr_table_xp_value))
            for cr, cr_table_xp_value in CR_EXPERIENCE_POINTS.items()
        ]
        min_dist = min(distances, key=lambda x: x[1])
        monster_cr = next((cr for cr, dist in distances if dist == min_dist[1]), None)
        if monster_cr is None:
            raise RuntimeError
        return monster_cr


class CreatureType(Enum):
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

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])

    @staticmethod
    def from_name(name: str) -> CreatureType:
        for mt in CreatureType:
            if name.lower() == mt.name.lower():
                return mt
        raise ValueError(f"Invalid monster type: {name}")

    @staticmethod
    def from_display_name(name: str) -> CreatureType:
        for mt in CreatureType:
            if mt.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return mt
        raise ValueError(f"invalid CreatureType: {name}")


class Alignment(Enum):
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

    @staticmethod
    def from_name(alignment_name: str) -> Alignment:
        for a in Alignment:
            if alignment_name.lower() == a.name.lower():
                return a
        raise ValueError(f"Invalid alignment: {alignment_name}")

    @staticmethod
    def from_display_name(name: str) -> Alignment:
        for a in Alignment:
            if a.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return a
        raise ValueError(f"invalid Alignment: {name}")

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])


class EncounterSize(Enum):
    SINGLETON = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    SWARM = auto()

    @property
    def num_creatures(self) -> int:
        match self:
            case EncounterSize.SINGLETON:
                return 1
            case EncounterSize.SMALL:
                # return randint(2, 4)
                return 3
            case EncounterSize.MEDIUM:
                # return randint(5, 8)
                return 6
            case EncounterSize.LARGE:
                # return randint(9, 12)
                return 10
            case EncounterSize.SWARM:
                # return randint(13, 20)
                return 15
            case _:
                raise NotImplementedError

    @staticmethod
    def from_name(size_name: str) -> EncounterSize:
        for es in EncounterSize:
            if es.name.lower() == size_name.lower():
                return es
        raise ValueError(f"invalid EncounterSize: {size_name}")

    @staticmethod
    def from_display_name(name: str) -> EncounterSize:
        for es in EncounterSize:
            if es.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return es
        raise ValueError(f"invalid EncounterSize: {name}")

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])


class EncounterDifficulty(Enum):
    LOW = auto()
    MODERATE = auto()
    HIGH = auto()

    def experience_points_budget(
        self, avg_party_level: int, num_players: int = 1
    ) -> int:
        xp_budget_per_player = ENCOUNTER_DIFFICULTY_XP_BUDGET[self].get(
            avg_party_level, 0
        )
        total_xp_budget_for_encounter = xp_budget_per_player * num_players
        return total_xp_budget_for_encounter

    @staticmethod
    def from_name(name: str) -> EncounterDifficulty:
        for ed in EncounterDifficulty:
            if ed.name.lower() == name.lower():
                return ed
        raise ValueError(f"invalid EncounterDifficulty: {name}")

    @staticmethod
    def from_display_name(name: str) -> EncounterDifficulty:
        for ed in EncounterDifficulty:
            if ed.name.lower() == "_".join([c for c in name.split(" ")]).lower():
                return ed
        raise ValueError(f"invalid EncounterDifficulty: {name}")

    @property
    def display_name(self) -> str:
        return " ".join([token.capitalize() for token in self.name.split("_")])


ENCOUNTER_DIFFICULTY_XP_BUDGET: dict[EncounterDifficulty, dict[int, int]] = {
    EncounterDifficulty.LOW: {
        1: 50,
        2: 100,
        3: 150,
        4: 250,
        5: 500,
        6: 600,
        7: 750,
        8: 1000,
        9: 1300,
        10: 1600,
        11: 1900,
        12: 2200,
        13: 2600,
        14: 2900,
        15: 3300,
        16: 3800,
        17: 4500,
        18: 5000,
        19: 5500,
        20: 6400,
    },
    EncounterDifficulty.MODERATE: {
        1: 75,
        2: 150,
        3: 225,
        4: 375,
        5: 750,
        6: 1000,
        7: 1300,
        8: 1700,
        9: 2000,
        10: 2300,
        11: 2900,
        12: 3700,
        13: 4200,
        14: 4900,
        15: 5400,
        16: 6100,
        17: 7200,
        18: 8700,
        19: 10700,
        20: 13200,
    },
    EncounterDifficulty.HIGH: {
        1: 100,
        2: 200,
        3: 400,
        4: 500,
        5: 1100,
        6: 1400,
        7: 1700,
        8: 2100,
        9: 2600,
        10: 3100,
        11: 4100,
        12: 4700,
        13: 5400,
        14: 6200,
        15: 7800,
        16: 9800,
        17: 11700,
        18: 14200,
        19: 17200,
        20: 22000,
    },
}


@dataclass
class Monster:
    name: str | None = field(default=None)
    description: str | None = field(default=None)
    habitat: str | None = field(default=None)
    treasure: str | None = field(default=None)
    artwork_url: str | None = field(default=None)
    creature_type: CreatureType | None = field(default=None)
    alignment: Alignment | None = field(default=None)
    tags: list[str] = field(default_factory=list)
    hit_dice: Dice | None = field(default=None)
    size: Size | None = field(default=None)
    speed: dict[SpeedType, int] = field(
        default_factory=lambda: {
            SpeedType.WALKING: 30,
            SpeedType.SWIM: 0,
            SpeedType.FLY: 0,
            SpeedType.CLIMB: 0,
            SpeedType.BURROW: 0,
        }
    )
    ability_scores: AbilityScores = field(
        default=AbilityScores({ability: 10 for ability in Ability})
    )
    skills: dict[Skill, Proficiency] = field(default_factory=dict)
    damage_resistances: dict[DamageType, Resistance] = field(default_factory=dict)
    saving_throws: dict[Ability, Proficiency] = field(
        default_factory=lambda: {ability: Proficiency.NORMAL for ability in Ability}
    )
    condition_resistances: dict[Condition, Resistance] = field(default_factory=dict)
    senses: dict[Sense, int] = field(default_factory=dict)
    languages: list[Language] = field(default_factory=list)
    telepathy: tuple[bool, int] | None = field(default=None)
    challenge_rating: ChallengeRating | None = field(default=None)

    def __post_init__(self) -> None:
        self.ac_tied_to_cr = True
        self.hp_tied_to_cr = True

    @property
    def in_lair(self) -> bool | None:
        if self._requirements_met("challenge_rating"):
            return self.challenge_rating.in_lair
        return None

    @in_lair.setter
    def in_lair(self, value: bool) -> None:
        if self._requirements_met("challenge_rating"):
            self.challenge_rating.in_lair = value

    @property
    def strength(self) -> int | None:
        if self._requirements_met("ability_scores"):
            return self.ability_scores.scores[Ability.STRENGTH]
        return None

    @property
    def strength_mod(self) -> int | None:
        if self._requirements_met("ability_scores"):
            return self.ability_scores.strength_modifier

    @property
    def strength_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.STRENGTH):
            return self.strength_mod + self.proficiency_bonus
        return self.strength_mod

    @property
    def dex(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.scores[Ability.DEXTERITY]

    @property
    def dex_mod(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.dexterity_modifier

    @property
    def dex_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.DEXTERITY):
            return self.dex_mod + self.proficiency_bonus
        return self.dex_mod

    @property
    def con(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.scores[Ability.CONSTITUTION]

    @property
    def con_mod(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.constitution_modifier

    @property
    def con_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.CONSTITUTION):
            return self.con_mod + self.proficiency_bonus
        return self.con_mod

    @property
    def intelligence(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.scores[Ability.INTELLIGENCE]

    @property
    def intelligence_mod(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.intelligence_modifier

    @property
    def intelligence_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.INTELLIGENCE):
            return self.intelligence_mod + self.proficiency_bonus
        return self.intelligence_mod

    @property
    def wis(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.scores[Ability.WISDOM]

    @property
    def wis_mod(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.wisdom_modifier

    @property
    def wis_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.WISDOM):
            return self.wis_mod + self.proficiency_bonus
        return self.wis_mod

    @property
    def cha(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.scores[Ability.CHARISMA]

    @property
    def cha_mod(self) -> int | None:
        if self.ability_scores is None:
            return None
        return self.ability_scores.charisma_modifier

    @property
    def cha_save(self) -> int | None:
        if self.ability_scores is None:
            return None
        if self._is_proficient_in_saving_throw(Ability.CHARISMA):
            return self.cha_mod + self.proficiency_bonus
        return self.cha_mod

    @property
    def proficiency_bonus(self) -> int | None:
        if self.challenge_rating is None:
            return None
        return self.challenge_rating.proficiency_bonus

    @property
    def passive_perception(self) -> int | None:
        if self._is_proficient_in_skill(Skill.PERCEPTION):
            pass
        return

    @property
    def initiative(self) -> str:
        return (
            f"+{self.dex_mod} ({self.dex})"
            if self.dex >= 10
            else f"-{self.dex_mod} ({self.dex})"
        )

    @property
    def ac_tied_to_cr(self) -> bool:
        return getattr(self, "_ac_tied_to_cr")

    @ac_tied_to_cr.setter
    def ac_tied_to_cr(self, value: bool) -> None:
        setattr(self, "_ac_tied_to_cr", value)

    @property
    def hp_tied_to_cr(self) -> bool:
        return getattr(self, "_hp_tied_to_cr")

    @hp_tied_to_cr.setter
    def hp_tied_to_cr(self, value: bool) -> None:
        setattr(self, "_hp_tied_to_cr", value)

    @property
    def ac(self) -> int | None:
        if self.ac_tied_to_cr:
            if not self._requirements_met("challenge_rating"):
                return None
            return self.challenge_rating.armor_class
        return getattr(self, "_ac")

    @ac.setter
    def ac(self, value: int) -> None:
        if self.ac_tied_to_cr:
            return
        setattr(self, "_ac", value)

    @property
    def hp(self) -> str | None:
        if self.hp_tied_to_cr:
            if not self._requirements_met(
                ["challenge_rating", "ability_scores", "size"]
            ):
                return None
            return self.challenge_rating.hit_points(self.ability_scores, self.size)
        return getattr(self, "_hp")

    @hp.setter
    def hp(self, value: str) -> None:
        if self.hp_tied_to_cr:
            return
        setattr(self, "_hp", value)

    def _is_proficient_in_skill(self, skill: Skill) -> bool:
        return (skill, Proficiency.PROFICIENT) in self.skills

    def _has_expertise_in_skill(self, skill: Skill) -> bool:
        return (skill, Proficiency.EXPERTISE) in self.skills

    def _is_proficient_in_saving_throw(self, ability: Ability) -> bool:
        saving_throw_proficiency = self.saving_throws.get(ability, None)
        if saving_throw_proficiency is None:
            return False
        return saving_throw_proficiency == Proficiency.PROFICIENT

    def _has_expertise_in_saving_throw(self, ability: Ability) -> bool:
        saving_throw_expertise = self.saving_throws.get(ability, None)
        if saving_throw_expertise is None:
            return False
        return saving_throw_expertise == Proficiency.EXPERTISE

    @property
    def tags_display(self) -> str:
        return ", ".join(self.tags) if self.tags else ""

    @property
    def speed_display(self) -> str:
        retval = ""
        walk_speed = f"{self.speed[SpeedType.WALKING]} ft."
        additional_speeds = []
        alphabetical_types = sorted(
            [s for s in SpeedType if s != SpeedType.WALKING],
            key=lambda x: x.name.lower(),
        )
        for speed_type in alphabetical_types:
            if self.speed[speed_type] != 0:
                additional_speeds.append(
                    f"{speed_type.name.capitalize()} {self.speed[speed_type]} ft."
                )
        if additional_speeds:
            additional_speeds.insert(0, walk_speed)
            retval = ", ".join(additional_speeds)
        else:
            retval = walk_speed
        return retval

    @property
    def skills_display(self) -> str:
        if not self._requirements_met(["ability_scores", "challenge_rating"]):
            return ""
        retval = []
        ab_sc = self.ability_scores
        for skill, proficiency in sorted(
            self.skills.items(), key=lambda x: x[0].display_name
        ):
            skill_mod = ab_sc._calculate_modifier(
                ab_sc.scores[skill.associated_ability]
            )
            pb = self.challenge_rating.proficiency_bonus
            match proficiency:
                case Proficiency.NORMAL:
                    total_bonus = skill_mod
                case Proficiency.PROFICIENT:
                    total_bonus = skill_mod + pb
                case Proficiency.EXPERTISE:
                    total_bonus = skill_mod + (2 * pb)
                case _:
                    raise NotImplementedError
            retval.append(f"{skill.display_name} +{total_bonus}")
        return ", ".join(retval)

    @property
    def resistances_display(self) -> str:
        dmg_resistances = sorted(
            [
                dt.display_name
                for dt, res in self.damage_resistances.items()
                if res == Resistance.RESISTANT
            ],
            key=lambda x: x.lower(),
        )
        return ", ".join(dmg_resistances)

    @property
    def senses_display(self) -> str:
        alphabetical_senses = sorted(
            [
                f"{sense.display_name} {range} ft."
                for sense, range in self.senses.items()
            ],
            key=lambda x: x.lower(),
        )
        return (
            ", ".join(alphabetical_senses)
            + "; "
            + f"Passive Perception {self.passive_perception}"
        )

    @property
    def immunities_display(self) -> str:
        dmg_immunities = sorted(
            [
                dt.display_name
                for dt, res in self.damage_resistances.items()
                if res == Resistance.IMMUNE
            ],
            key=lambda x: x.lower(),
        )
        condition_immunities = sorted(
            [
                condition.display_name
                for condition, resistance in self.condition_resistances.items()
                if resistance == Resistance.IMMUNE
            ],
            key=lambda x: x.lower(),
        )
        return ", ".join(dmg_immunities) + "; " + ", ".join(condition_immunities)

    @property
    def languages_display(self) -> str:
        return ", ".join([l.display_name for l in self.languages])

    @property
    def traits_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def actions_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def bonus_actions_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def reactions_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def legendary_actions_display(self) -> str:
        return ""  # TODO: Implement me

    def _requirements_met(self, required_fields: Sequence[str]) -> bool:
        return not any(
            (
                getattr(self, required_field, None) is None
                for required_field in required_fields
            )
        )

    def as_homebrewery_v3_markdown(self, wide_statblock: bool = False) -> str:
        return (
            f"{{{{monster,frame{',wide' if wide_statblock else ''}\n"
            f"## {self.name}\n"
            f"*{self.size.display_name} {self.creature_type.display_name}{self.tags_display}, {self.alignment.display_name}*\n"
            "\n"
            "{{stats\n"
            "\n"
            "{{vitals\n"
            f"**AC** :: {self.ac}\n"
            f"**HP** :: {self.hp}\n"
            f"**Speed** :: {self.speed_display}\n"
            "\column\n"
            f"**Initiative** :: {self.initiative}\n"
            "}}\n"
            "\n"
            "{{tables\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Str| {self.strength} | {self.strength_mod} | {self.strength_save} |\n"
            f"|Int| {self.intelligence} | {self.intelligence_mod} | {self.intelligence_save} |\n"
            "\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Dex| {self.dex} | {self.dex_mod} | {self.dex_save} |\n"
            f"|Wis| {self.wis} | {self.wis_mod} | {self.wis_save} |\n"
            "\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Con| {self.con} | {self.con_mod} | {self.con_save} |\n"
            f"|Cha| {self.cha} | {self.cha_mod} | {self.cha_save} |\n"
            "}}\n"
            "\n"
            f"**Skills** :: {self.skills_display}\n"
            f"**Resistances** :: {self.resistances_display}\n"
            f"**Senses** :: {self.senses_display}\n"
            f"**Languages** :: {self.languages_display}\n"
            f"**CR** :: {self.challenge_rating.display}\n"
            "}}\n"
            "\n"
            "### Traits\n"
            f"{self.traits_display}\n"  # TODO: Implement me
            "### Actions\n"
            f"{self.actions_display}\n"  # TODO: Implement me
            "\n"
            "}}\n"
        )
