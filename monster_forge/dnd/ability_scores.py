from enum import auto
from monster_forge.dnd.enums import DNDEnum
import math
from dataclasses import dataclass
from monster_forge.dnd.enums import Ability


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
