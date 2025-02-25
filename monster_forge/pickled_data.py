from dataclasses import dataclass
from monster_forge.dnd.dnd import Encounter, Monster


@dataclass
class PickledMonsterData:
    monster: Monster
    encounter: Encounter
