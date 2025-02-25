from collections.abc import Sequence
from monster_forge.dnd.enums import (
    Size,
    Alignment,
)
from monster_forge.dnd.monster import Monster
from monster_forge.dnd.encounter import Encounter, EncounterDifficulty, EncounterSize
from monster_forge.openai_local.openai_agent import OpenAIAgent
from monster_forge.utilities import yes_or_no_question, numbered_choice


class MonsterMaker:
    def __init__(self) -> None:
        self._openai_agent = OpenAIAgent()
        pass

    def create_monster(self) -> Monster:
        while True:
            if not yes_or_no_question("Would you like to create a monster?"):
                break
            concept = self.get_monster_concept()
            name = self.get_monster_name(concept)
            size = self.get_monster_size()
            alignment = self.get_monster_alignment()
            # TODO: Get monster type
            # TODO: Get a description
            # TODO: Get a habitat
            # TODO: Get treasure
            # TODO: Provide tags if any
            encounter_stats = self.get_monster_encounter_stats()
            # TODO: Determine stats based on CR
            # TODO: Calculate hit dice based on stats
            # TODO: Determine speed(s)
            # TODO: Determine languages / telepathy & range
            # TODO: Determine damage vulnerabilities/resistances/immunities
            # TODO: Determine condition immunities
            # TODO: Determine senses and ranges
            # TODO: Generate artwork
            print("Done!")

    def get_monster_concept(self) -> str:
        monster_concept = input(
            "Please enter a general concept for the monster you want to create: "
        )
        refine_concept = yes_or_no_question(
            "Would you like me to refine the concept for you?: "
        )
        if refine_concept:
            monster_concept = self.refine_monster_concept(monster_concept)
        return monster_concept

    def get_monster_name(self, monster_concept: str) -> str:
        suggest_names = yes_or_no_question(
            "Would you like me to suggest names for the monster?: "
        )
        monster_name = None
        if suggest_names:
            suggested_names = self.suggest_names(monster_concept)
            monster_name = numbered_choice(
                suggested_names,
                prompt="Please select one of the following name suggestions:",
            )
        else:
            monster_name = input("Please provide a name for the monster: ")
            monster_name = " ".join(
                token.capitalize() for token in monster_name.lower()
            )

    def get_monster_size(self) -> Size:
        return Size.from_name(
            numbered_choice([s.name for s in Size], prompt="What size is this monster?")
        )

    def get_monster_alignment(self) -> Alignment:
        return Alignment.from_name(
            numbered_choice(
                [a.name for a in Alignment],
                prompt="What is this monster's alignment?",
            )
        )

    def get_monster_encounter_stats(self) -> Encounter:
        player_levels = (
            input(
                "What are your player's levels? (Enter a comma separated list of levels): "
            )
            .replace(" ", "")
            .strip()
            .split(",")
        )
        player_levels = [int(pl) for pl in player_levels]
        encounter_size = EncounterSize.from_name(
            numbered_choice(
                [es.name for es in EncounterSize],
                prompt="What size encounter would you like?",
            )
        )
        encounter_difficulty = EncounterDifficulty.from_name(
            numbered_choice(
                [ed.name for ed in EncounterDifficulty],
                prompt="What difficulty encounter would you like?",
            )
        )
        encounter = Encounter(player_levels, encounter_difficulty, encounter_size)
        return encounter

    def refine_monster_concept(self, original_concept: str) -> str:
        refined_concept = self._openai_agent.generate_text(
            f"Please refine and enhance the following D&D 5e 2024 monster concept: {original_concept}. Your answer must be a single descriptive block of text, no more than 4 sentences."
        )
        print(f"Monster concept refined: {refined_concept}")
        return refined_concept

    def suggest_names(self, monster_concept: str, num_names: int = 1) -> Sequence[str]:
        csv_suggested_names = self._openai_agent.generate_text(
            f"Please suggest {num_names} unique, diverse and interesting names for a D&D 5E 2024 monster based on the following concept: {monster_concept}. These names should evoke thoughts and feelings related to the concept of the monster. Some should be simple names and others more complicated. Your response must simply be the {num_names} suggestions, formatted as a comma separated list of the names with no other text whatsoever."
        )
        suggested_names = csv_suggested_names.split(", ")
        return [
            " ".join([word.capitalize() for word in suggested_name.split(" ")])
            for suggested_name in suggested_names
        ]
