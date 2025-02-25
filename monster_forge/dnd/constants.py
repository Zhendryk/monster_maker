from typing import Final
from monster_forge.dnd.enums import (
    Condition,
    DamageType,
    Sense,
    Skill,
    Ability,
    Size,
    CreatureType,
)

PHRASES_TO_CAPITALIZE: Final[list[str]] = (
    [c.display_name for c in Condition]
    + [dt.display_name for dt in DamageType]
    + [s.display_name for s in Sense]
    + [s.display_name for s in Skill]
    + [a.display_name for a in Ability]
    + [s.display_name for s in Size]
    + [ct.display_name for ct in CreatureType]
)

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
