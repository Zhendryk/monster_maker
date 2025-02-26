from dataclasses import dataclass, field
from monster_forge.dnd.enums import LimitedUsageType, Die, Ability, Proficiency
import re
from monster_forge.dnd.constants import (
    PHRASES_TO_CAPITALIZE,
    MACRO_MONSTER_NAME,
    MACRO_STR_MOD,
    MACRO_DEX_MOD,
    MACRO_CON_MOD,
    MACRO_INT_MOD,
    MACRO_WIS_MOD,
    MACRO_CHA_MOD,
    PATTERN_DICE_ROLL,
    PATTERN_DICE_ROLL_CG_NUM_DICE,
    PATTERN_DICE_ROLL_CG_DIE_TYPE,
    PATTERN_DICE_ROLL_CG_SIGN,
    PATTERN_DICE_ROLL_CG_BONUS,
    PATTERN_STAT_OPERATION,
    PATTERN_STAT_OPERATION_CG_STAT,
    PATTERN_STAT_OPERATION_CG_OPERATION,
    PATTERN_STAT_OPERATION_CG_SIGN,
    PATTERN_STAT_OPERATION_CG_BONUS,
)
from monster_forge.dnd.dice import Dice
from monster_forge.dnd.ability_scores import AbilityScores


@dataclass
class Trait:
    host_creature_name: str
    ability_scores: AbilityScores
    proficiency_bonus: int
    saving_throws: dict[Ability, Proficiency]
    title: str
    description: str
    limited_use_type: LimitedUsageType = field(default=LimitedUsageType.UNLIMITED)
    limited_use_charges: dict[str, int] = field(default_factory=dict)
    has_lair: bool = field(default=False)
    lair_charge_bonuses: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.host_creature_name = " ".join(
            [c.capitalize() for c in self.host_creature_name.split(" ")]
        )
        self.title = " ".join([c.capitalize() for c in self.title.split(" ")])
        self._format_description()
        if (
            self.limited_use_type == LimitedUsageType.X_PER_DAY
            and "x" not in self.limited_use_charges
        ):
            raise ValueError(
                "x required in limited use charges if making a X_PER_DAY trait"
            )
        if self.limited_use_type == LimitedUsageType.RECHARGE_X_Y and (
            "x" not in self.limited_use_charges or "y" not in self.limited_use_charges
        ):
            raise ValueError(
                "x and y required in limited use charges if making a RECHARGE_X_Y trait"
            )

    def _substitute_dice_roll(self, match: re.Match) -> str:
        num_dice = int(match.group(PATTERN_DICE_ROLL_CG_NUM_DICE))
        die_type = Die.from_name(match.group(PATTERN_DICE_ROLL_CG_DIE_TYPE))
        sign = match.group(PATTERN_DICE_ROLL_CG_SIGN)
        bonus = match.group(PATTERN_DICE_ROLL_CG_BONUS)
        if bonus is not None:
            bonus = int(bonus)
        dice_roll_calculated = Dice.calculate_avg_roll(num_dice, die_type, sign, bonus)
        return str(dice_roll_calculated)

    def _substitute_stat_operation(self, match: re.Match) -> str:
        stat = match.group(PATTERN_STAT_OPERATION_CG_STAT)
        operation = match.group(PATTERN_STAT_OPERATION_CG_OPERATION)
        sign = match.group(PATTERN_STAT_OPERATION_CG_SIGN)
        bonus = match.group(PATTERN_STAT_OPERATION_CG_BONUS)
        if bonus is not None:
            bonus = int(bonus)
        stat_operation_calculated = self.ability_scores.calculate_stat_operation(
            self.proficiency_bonus,
            self.saving_throws,
            stat,
            operation,
            sign=sign,
            bonus=bonus,
        )
        return str(stat_operation_calculated)

    def _resolve_macros(self) -> None:
        self.description = PATTERN_DICE_ROLL.sub(
            self._substitute_dice_roll, self.description
        )
        self.description = PATTERN_STAT_OPERATION.sub(
            self._substitute_stat_operation, self.description
        )
        self.description = self.description.replace(
            MACRO_MONSTER_NAME, self.host_creature_name
        )
        self.description = self.description.replace(
            MACRO_STR_MOD, str(self.ability_scores.strength_modifier)
        )
        self.description = self.description.replace(
            MACRO_DEX_MOD, str(self.ability_scores.dexterity_modifier)
        )
        self.description = self.description.replace(
            MACRO_CON_MOD, str(self.ability_scores.constitution_modifier)
        )
        self.description = self.description.replace(
            MACRO_INT_MOD, str(self.ability_scores.intelligence_modifier)
        )
        self.description = self.description.replace(
            MACRO_WIS_MOD, str(self.ability_scores.wisdom_modifier)
        )
        self.description = self.description.replace(
            MACRO_CHA_MOD, str(self.ability_scores.charisma_modifier)
        )

    def _format_description(self) -> None:
        self.description = self.description.strip().rstrip(".")
        self._resolve_macros()
        for phrase_to_capitalize in PHRASES_TO_CAPITALIZE:
            self.description = self.description.replace(
                phrase_to_capitalize, phrase_to_capitalize.capitalize()
            )
        pieces = self.description.split(" ")
        pieces[0] = pieces[0].capitalize()
        self.description = " ".join(pieces)

    @property
    def limited_usage_str(self) -> str:
        if self.limited_use_type == LimitedUsageType.UNLIMITED:
            return ""
        match self.limited_use_type:
            case LimitedUsageType.X_PER_DAY:
                x = self.limited_use_charges["x"]
                if self.has_lair:
                    x_bonus = self.lair_charge_bonuses["x"]
                    return f"({x}/Day, or {x + x_bonus}/Day in Lair)"
                return f"({x}/Day)"
            case LimitedUsageType.RECHARGE_X_Y:
                x = self.limited_use_charges["x"]
                y = self.limited_use_charges["y"]
                return f"(Recharge {x}-{y})"
            case LimitedUsageType.RECHARGE_AFTER_SHORT_OR_LONG_REST:
                return "(Recharge after a Short or Long Rest)"
            case _:
                raise NotImplementedError

    def as_homebrewery_v3_2024_markdown(self) -> str:
        return f"***{self.title}{' ' + self.limited_usage_str if self.limited_usage_str else ''}.*** {self.description}."

    def display_str(self) -> str:
        return f"{self.title}{' ' + self.limited_usage_str if self.limited_usage_str else ''}. {self.description}."


@dataclass
class LegendaryResistance(Trait):
    title: str = field(default="Legendary Resistance")
    description: str = field(
        default="If the [MON] fails a saving throw, it can choose to succeed instead."
    )
    limited_use: bool = field(default=True)
    limited_use_type: LimitedUsageType = field(default=LimitedUsageType.X_PER_DAY)
    limited_use_charges: dict[str, int] = field(default_factory=lambda: {"x": 3})
