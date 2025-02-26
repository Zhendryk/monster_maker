from dataclasses import dataclass, field
import re
from monster_forge.dnd.enums import (
    ActionSubtype,
    Ability,
    Proficiency,
    LimitedUsageType,
    Die,
)
from typing import Any
from monster_forge.dnd.ability_scores import AbilityScores
from monster_forge.dnd.damage import Damage
from monster_forge.dnd.dice import Dice
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
    PATTERN_STAT_ATTACK,
    PATTERN_STAT_ATTACK_CG_STAT,
    PATTERN_STAT_ATTACK_CG_NUM_DICE,
    PATTERN_STAT_ATTACK_CG_DIE_TYPE,
    PATTERN_STAT_ATTACK_CG_SIGN,
    PATTERN_STAT_ATTACK_CG_BONUS,
)


@dataclass
class CombatCharacteristic:
    monster_name: str
    ability_scores: AbilityScores
    proficiency_bonus: int
    saving_throws: dict[Ability, Proficiency]
    has_lair: bool
    title: str
    description: str

    def __post_init__(self) -> None:
        self.monster_name = " ".join(
            [c.capitalize() for c in self.monster_name.split(" ")]
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

    def _substitute_dice_roll(self, match: re.Match, add_sign: bool = False) -> str:
        num_dice = int(match.group(PATTERN_DICE_ROLL_CG_NUM_DICE))
        die_type = Die.from_name(match.group(PATTERN_DICE_ROLL_CG_DIE_TYPE))
        sign = match.group(PATTERN_DICE_ROLL_CG_SIGN)
        bonus = match.group(PATTERN_DICE_ROLL_CG_BONUS)
        if bonus is not None:
            bonus = int(bonus)
        dice_roll_calculated = Dice.calculate_avg_roll(num_dice, die_type, sign, bonus)
        if add_sign:
            return (
                f"+{dice_roll_calculated}"
                if dice_roll_calculated >= 0
                else f"-{dice_roll_calculated}"
            )
        return str(dice_roll_calculated)

    def _substitute_stat_attack(self, match: re.match, add_sign: bool = True) -> str:
        stat = Ability.from_abbreviation(match.group(PATTERN_STAT_ATTACK_CG_STAT))
        num_dice = int(match.group(PATTERN_STAT_ATTACK_CG_NUM_DICE))
        die_type = Die.from_name(match.group(PATTERN_STAT_ATTACK_CG_DIE_TYPE))
        sign = match.group(PATTERN_STAT_ATTACK_CG_SIGN)
        bonus = match.group(PATTERN_STAT_ATTACK_CG_BONUS)
        calced_bonus = 0
        if sign and bonus is not None:
            match sign:
                case "+":
                    calced_bonus = abs(bonus)
                case "-":
                    calced_bonus = -abs(bonus)
                case _:
                    raise NotImplementedError
        dice = Dice({die_type: num_dice})
        attack_bonus = (
            self.ability_scores._calculate_modifier(self.ability_scores.scores[stat])
            + self.proficiency_bonus
            + calced_bonus
        )
        damage_roll_calculated = dice.average_value + attack_bonus
        if add_sign:
            return (
                f"+{damage_roll_calculated}"
                if damage_roll_calculated >= 0
                else f"-{damage_roll_calculated}"
            )
        return str(damage_roll_calculated)

    def _substitute_stat_operation(self, match: re.Match, add_sign: bool = True) -> str:
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
        if add_sign:
            return (
                f"+{stat_operation_calculated}"
                if stat_operation_calculated >= 0
                else f"-{stat_operation_calculated}"
            )
        return str(stat_operation_calculated)

    def _resolve_macros(self) -> None:
        self.description = PATTERN_DICE_ROLL.sub(
            self._substitute_dice_roll, self.description
        )
        self.description = PATTERN_STAT_ATTACK.sub(
            self._substitute_stat_attack, self.description
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
    def homebrewery_v3_2024_markdown(self) -> str:
        return f"***{self.title}.*** {self.description}"


@dataclass
class Trait(CombatCharacteristic):
    limited_use_type: LimitedUsageType = field(default=LimitedUsageType.UNLIMITED)
    limited_use_charges: dict[str, int] = field(default_factory=dict)
    lair_charge_bonuses: dict[str, int] = field(default_factory=dict)


@dataclass
class Action(CombatCharacteristic):
    subtype: ActionSubtype | None


@dataclass
class Multiattack(Action):
    @staticmethod
    def templates(**kwargs: dict[str, Any]) -> list[tuple[str, str]]:
        return [
            (
                "Multiattack (Action)",
                "The [MON] makes two ??? attacks.",
            )
        ]


@dataclass
class MeleeAttackRoll(Action):
    @staticmethod
    def templates(**kwargs: dict[str, Any]) -> list[tuple[str, str]]:
        ability: Ability = kwargs["ability"]
        return [
            (
                f"{ability.abbreviation} Melee Attack Roll",
                f"_Melee Attack Roll:_ [{ability.abbreviation} ATK], reach ??? ft. _Hit:_ [{ability.abbreviation} ???D???] ??? damage.",
            )
        ]


@dataclass
class RangedAttackRoll(Action):
    @staticmethod
    def templates(**kwargs: dict[str, Any]) -> list[tuple[str, str]]:
        ability: Ability = kwargs["ability"]
        return [
            (
                f"{ability.abbreviation} Ranged Attack Roll",
                f"Ranged Attack Roll:_ [{ability.abbreviation} ATK], range ??? ft. _Hit:_ [{ability.abbreviation} ???D???] ??? damage.",
            )
        ]


@dataclass
class MeleeOrRangedAttackRoll(Action):
    @staticmethod
    def templates(**kwargs: dict[str, Any]) -> list[tuple[str, str]]:
        ability: Ability = kwargs["ability"]
        return [
            (
                f"{ability.abbreviation} Melee or Ranged Attack Roll",
                f"Melee or Ranged Attack Roll:_ [{ability.abbreviation} ATK], reach ??? ft. or range ??? ft. _Hit:_ [{ability.abbreviation} ???D???] ??? damage.",
            )
        ]


@dataclass
class SavingThrow(Action):
    @staticmethod
    def templates(**kwargs: dict[str, Any]) -> list[tuple[str, str]]:
        ability: Ability = kwargs["ability"]
        return [
            (
                f"{ability.name.capitalize()} Saving Throw",
                f"_{ability.name.capitalize()} Saving Throw:_ DC ???. _Failure:_ ???. _Success:_ ???. _Failure or Success:_ ???.",
            ),
            (
                f"Targeted {ability.name.capitalize()} Saving Throw",
                f"_{ability.name.capitalize()} Saving Throw:_ DC ???, one creature that ???. _Failure:_ ???. _Success:_ ???. _Failure or Success:_ ???.",
            ),
        ]


def all_action_templates() -> dict[str, str]:
    retval = {template[0]: template[1] for template in Multiattack.templates()}
    for ability in [Ability.STRENGTH, Ability.DEXTERITY]:
        for action in [MeleeAttackRoll, RangedAttackRoll, MeleeOrRangedAttackRoll]:
            templates = action.templates(ability=ability)
            for template in templates:
                retval[template[0]] = template[1]
    for ability in Ability:
        templates = SavingThrow.templates(ability=ability)
        for template in templates:
            retval[template[0]] = template[1]
    return retval
