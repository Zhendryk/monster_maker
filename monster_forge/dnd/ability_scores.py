import math
from dataclasses import dataclass
from monster_forge.dnd.enums import Ability, Proficiency

STAT_STR_TO_ABILITY: dict[str, Ability] = {
    "STR": Ability.STRENGTH,
    "DEX": Ability.DEXTERITY,
    "CON": Ability.CONSTITUTION,
    "INT": Ability.INTELLIGENCE,
    "WIS": Ability.WISDOM,
    "CHA": Ability.CHARISMA,
}


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

    @property
    def display_str(self) -> str:
        return ", ".join(
            [
                f"{ability.display_name}:{score}"
                for ability, score in self.scores.items()
            ]
        )

    def calculate_stat_operation(
        self,
        proficiency_bonus: int,
        saving_throws: dict[Ability, Proficiency],
        stat: str,
        operation: str,
        sign: str | None = None,
        bonus: int | None = None,
    ) -> int:
        ability = STAT_STR_TO_ABILITY[stat]
        ability_mod = self._calculate_modifier(self.scores[ability])
        calced_bonus = 0
        if sign and bonus is not None:
            match sign:
                case "+":
                    calced_bonus = abs(bonus)
                case "-":
                    calced_bonus = -abs(bonus)
                case _:
                    raise NotImplementedError
        match operation:
            case "ATK":
                return proficiency_bonus + ability_mod + calced_bonus
            case "SAVE":
                if saving_throws[ability] != Proficiency.NORMAL:
                    return proficiency_bonus + ability_mod + calced_bonus
                return ability_mod + calced_bonus
            case _:
                pass
