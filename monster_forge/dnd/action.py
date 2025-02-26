from dataclasses import dataclass, field
from monster_forge.dnd.enums import ActionSubtype, Ability
from monster_forge.dnd.ability_scores import AbilityScores
from monster_forge.dnd.damage import Damage


@dataclass
class Action:
    title: str
    description: str
    subtype: ActionSubtype | None


@dataclass
class Attack(Action):
    proficiency_bonus: int
    primary_stat: Ability
    ability_scores: AbilityScores
    damage: list[Damage]
    additional_effect: str | None

    @property
    def primary_stat_bonus(self) -> int:
        return self.ability_scores._calculate_modifier(
            self.ability_scores.scores[self.primary_stat]
        )

    @property
    def hit_bonus(self) -> int:
        return self.proficiency_bonus + self.primary_stat_bonus

    @property
    def dmg_str(self) -> str:
        return (
            " plus ".join([dmg.homebrewery_v3_2024_markdown for dmg in self.damage])
            + "."
        )


@dataclass
class Multiattack(Action):
    title: str = field(default="Multiattack")
    subtype: ActionSubtype | None = field(default=None)


@dataclass
class MeleeAttackRoll(Attack):
    reach_ft: int
    additional_effect: str | None = field(default=None)
    subtype: ActionSubtype = field(default=ActionSubtype.MELEE_ATTACK_ROLL)

    @property
    def homebrewery_v3_2024_markdown(self) -> str:
        retval = f"***{self.title}.*** _{self.subtype.display_name}:_"
        retval = f"{retval} {'+' + self.hit_bonus if self.hit_bonus >= 0 else '-' + self.hit_bonus}, reach {self.reach_ft} ft. _Hit:_ {self.dmg_str}.{' ' + self.additional_effect if self.additional_effect else ''}"
        return retval


@dataclass
class RangedAttackRoll(Attack):
    range_ft: int
    additional_effect: str | None = field(default=None)
    subtype: ActionSubtype = field(default=ActionSubtype.RANGED_ATTACK_ROLL)

    @property
    def homebrewery_v3_2024_markdown(self) -> str:
        retval = f"***{self.title}.*** _{self.subtype.display_name}:_"
        retval = f"{retval} {'+' + self.hit_bonus if self.hit_bonus >= 0 else '-' + self.hit_bonus}, range {self.reach_ft} ft. _Hit:_ {self.dmg_str}.{' ' + self.additional_effect if self.additional_effect else ''}"
        return retval


@dataclass
class MeleeOrRangedAttackRoll(Attack):
    reach_ft: int
    range_ft: int
    subtype: ActionSubtype = field(default=ActionSubtype.MELEE_OR_RANGED_ATTACK_ROLL)

    @property
    def homebrewery_v3_2024_markdown(self) -> str:
        retval = f"***{self.title}.*** _{self.subtype.display_name}:_"
        retval = f"{retval} {'+' + self.hit_bonus if self.hit_bonus >= 0 else '-' + self.hit_bonus}, reach {self.reach_ft} ft. or range {self.range_ft} ft. _Hit:_ {self.dmg_str}.{' ' + self.additional_effect if self.additional_effect else ''}"
        return retval


@dataclass
class SavingThrow(Action):
    dc: int
    target: str | None = field(default=None)
    failure: str | None = field(default=None)
    success: str | None = field(default=None)
    failure_or_success: str | None = field(default=None)

    @property
    def homebrewery_v3_2024_markdown(self) -> str:
        retval = f"***{self.title}.*** _{self.subtype.display_name}:_ DC {self.dc}."
        if self.target:
            retval = f"{retval.rstrip('.', count=1)}, {self.target}."
        if self.failure_or_success:
            retval = f"{retval} _Failure or Success:_ {self.failure_or_success}"
            return retval
        else:
            if self.failure:
                retval = f"{retval} _Failure:_ {self.failure}."
            if self.success:
                retval = f"{retval} _Success:_ {self.success}."
            return retval
