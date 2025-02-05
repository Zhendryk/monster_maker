from __future__ import annotations
import math
from random import randint
from enum import Enum, auto
from dataclasses import dataclass
from collections.abc import Sequence
from functools import cached_property


class Sense(Enum):
    BLINDSIGHT = auto()
    DARKVISION = auto()
    TREMORSENSE = auto()
    TRUESIGHT = auto()


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


class Resistance(Enum):
    NORMAL = auto()
    VULNERABLE = auto()
    RESISTANT = auto()
    IMMUNE = auto()


class Proficiency(Enum):
    NORMAL = auto()
    PROFICIENT = auto()
    EXPERTISE = auto()


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


class SpeedType(Enum):
    WALKING = auto()
    BURROW = auto()
    CLIMB = auto()
    FLY = auto()
    SWIM = auto()


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


class Ability(Enum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()


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


@dataclass
class ChallengeRating(Enum):

    rating: int | float

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
    def experience_points(self) -> int:
        return CR_EXPERIENCE_POINTS[self.rating]

    def calculate_encounter_cr(
        self,
        avg_party_level: int,
        num_players: int,
        difficulty: EncounterDifficulty,
        size: EncounterSize,
    ) -> ChallengeRating:
        total_xp_budget = difficulty.experience_points_budget(
            avg_party_level, num_players=num_players
        )
        xp_per_creature = total_xp_budget / size.num_creatures


@dataclass
class Encounter:
    player_levels: Sequence[int]
    difficulty: EncounterDifficulty
    size: EncounterSize

    @cached_property
    def avg_party_level(self) -> int:
        return math.floor(sum(self.player_levels) / self.num_players)

    @cached_property
    def num_players(self) -> int:
        return len(self.player_levels)

    @cached_property
    def num_monsters(self) -> int:
        return self.size.num_creatures

    @cached_property
    def monster_cr(self) -> int | float:
        total_xp_budget = self.difficulty.experience_points_budget(
            self.avg_party_level, num_players=self.num_players
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


class MonsterType(Enum):
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
                return randint(2, 4)
            case EncounterSize.MEDIUM:
                return randint(5, 8)
            case EncounterSize.LARGE:
                return randint(9, 12)
            case EncounterSize.SWARM:
                return randint(13, 20)
            case _:
                raise NotImplementedError

    @staticmethod
    def from_name(size_name: str) -> EncounterSize:
        for es in EncounterSize:
            if es.name.lower() == size_name.lower():
                return es
        raise ValueError(f"invalid EncounterSize: {size_name}")


class EncounterDifficulty(Enum):
    LOW = auto()
    MODERATE = auto()
    HIGH = auto()

    def experience_points_budget(
        self, avg_party_level: int, num_players: int = 1
    ) -> int:
        xp_budget_per_player = ENCOUNTER_DIFFICULTY_XP_BUDGET[self][avg_party_level]
        total_xp_budget_for_encounter = xp_budget_per_player * num_players
        return total_xp_budget_for_encounter

    @staticmethod
    def from_name(difficulty_name: str) -> EncounterDifficulty:
        for ed in EncounterDifficulty:
            if ed.name.lower() == difficulty_name.lower():
                return ed
        raise ValueError(f"invalid EncounterDifficulty: {difficulty_name}")


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
    name: str
    description: str
    habitat: str
    treasure: str
    artwork_url: str
    monster_type: MonsterType
    alignment: Alignment
    tags: Sequence[str]
    hit_dice: Dice
    size: Size
    speed: dict[SpeedType, int]
    ability_scores: AbilityScores
    skills: dict[Skill, Proficiency]
    damage_resistances: dict[DamageType, Resistance]
    saving_throws: dict[Ability, Proficiency]
    condition_resistances: dict[Condition, Resistance]
    senses: dict[Sense, int]
    languages: Sequence[Language]
    telepathy: tuple[bool, int]
    challenge_rating: ChallengeRating

    @property
    def proficiency_bonus(self) -> int:
        return self.challenge_rating.proficiency_bonus

    @property
    def experience_points(self) -> int:
        return self.challenge_rating.experience_points

    def to_homebrewery_markdown(self) -> str:
        pass
