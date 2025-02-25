from dataclasses import dataclass
from monster_forge.dnd.monster import Monster
from monster_forge.dnd.encounter import Encounter


@dataclass
class PickledMonsterData:
    monster: Monster
    encounter: Encounter
