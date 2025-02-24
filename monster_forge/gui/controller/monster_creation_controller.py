from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from collections.abc import Sequence
from PyQt5.QtCore import QObject, Qt
import os
from monster_forge.gui.view.create_monster_view import Ui_CreateMonsterView
from monster_forge.monster_maker import MonsterMaker
from monster_forge.dnd.dnd import (
    Alignment,
    EncounterDifficulty,
    EncounterSize,
    Skill,
    Language,
    Condition,
    CreatureType,
    Size,
    DamageType,
    ChallengeRating,
    Encounter,
    Proficiency,
    Resistance,
    AbilityScores,
    Ability,
    SpeedType,
    Sense,
    Monster,
)
from pathlib import Path
from functools import partial
from random import randint

# Masquerade Demon
# A demon who blends into the higher eschelons of society to hunt its prey. It regularly attends soirees and other elegant events to lure victims in with its charming personality and impeccable decorum.


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_CreateMonsterView()
        self._view.setupUi(self)
        self.monster = Monster()
        self.encounter = Encounter()
        self._mm = MonsterMaker()
        self._setup_UI()
        self._output_folder: Path = (
            Path(__file__).parent.parent.parent.parent / "generated_output"
        )

    def _setup_UI(self) -> None:
        # Title
        self.setWindowTitle("Create New Monster")
        # Setting visibilty/enabled status of various components
        self._view.progressbar_ai_query.setVisible(False)
        self._view.lineedit_challenge_rating.setEnabled(False)
        # Combobox item population
        self._view.cb_skills.addItems(sorted([s.display_name for s in Skill]))
        self._view.cb_skills.setCurrentIndex(-1)
        self._view.cb_alignment.addItems(
            sorted([alignment.display_name for alignment in Alignment])
        )
        self._view.cb_alignment.setCurrentIndex(-1)
        self._view.cb_encounter_difficulty.addItems(
            sorted([diff.display_name for diff in EncounterDifficulty])
        )
        self._view.cb_encounter_difficulty.setCurrentIndex(-1)
        self._view.cb_encounter_size.addItems(
            sorted([size.display_name for size in EncounterSize])
        )
        self._view.cb_encounter_size.setCurrentIndex(-1)
        self._view.cb_conditions.addItems(
            sorted([condition.display_name for condition in Condition])
        )
        self._view.cb_conditions.setCurrentIndex(-1)
        self._view.cb_creature_type.addItems(
            sorted([mt.display_name for mt in CreatureType])
        )
        self._view.cb_creature_type.setCurrentIndex(-1)
        language_items = []
        for l in Language:
            language_items.append(l.display_name)
            if l.plus_amt > 0:
                items_to_Add = [l.display_name_plus_x(i) for i in range(1, l.plus_amt)]
                language_items.extend(items_to_Add)
        language_items.append("All")
        self._view.cb_languages.addItems(sorted(language_items))
        self._view.cb_languages.setCurrentIndex(-1)
        self._view.cb_senses.addItems(sorted([s.display_name for s in Sense]))
        self._view.cb_senses.setCurrentIndex(-1)
        self._view.cb_size.addItems(sorted([s.display_name for s in Size]))
        self._view.cb_size.setCurrentIndex(-1)
        self._view.cb_size.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_damage.addItems(sorted([d.display_name for d in DamageType]))
        self._view.cb_damage.setCurrentIndex(-1)
        # Combobox callbacks
        self._view.cb_encounter_size.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_encounter_difficulty.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_size.currentTextChanged.connect(self._size_changed)
        self._view.cb_alignment.currentTextChanged.connect(self._alignment_changed)
        self._view.cb_creature_type.currentTextChanged.connect(
            self._creature_type_changed
        )
        # Spinbox callbacks
        self._view.spinbox_avg_party_level.valueChanged.connect(self._calc_cr)
        self._view.spinbox_num_pcs.valueChanged.connect(self._calc_cr)
        self._view.spinbox_telepathy_range.valueChanged.connect(
            self._telepathy_range_changed
        )
        self._view.spinbox_walk_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.WALKING)
        )
        self._view.spinbox_swim_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.SWIM)
        )
        self._view.spinbox_fly_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.FLY)
        )
        self._view.spinbox_climb_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.CLIMB)
        )
        self._view.spinbox_burrow_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.BURROW)
        )
        self._view.spinbox_str.valueChanged.connect(
            partial(self._ability_score_changed, Ability.STRENGTH)
        )
        self._view.spinbox_dex.valueChanged.connect(
            partial(self._ability_score_changed, Ability.DEXTERITY)
        )
        self._view.spinbox_con.valueChanged.connect(
            partial(self._ability_score_changed, Ability.CONSTITUTION)
        )
        self._view.spinbox_int.valueChanged.connect(
            partial(self._ability_score_changed, Ability.INTELLIGENCE)
        )
        self._view.spinbox_wis.valueChanged.connect(
            partial(self._ability_score_changed, Ability.WISDOM)
        )
        self._view.spinbox_cha.valueChanged.connect(
            partial(self._ability_score_changed, Ability.CHARISMA)
        )
        self._view.spinbox_ac.valueChanged.connect(self._ac_changed)

        # Button actions
        self._view.btn_suggest_name.clicked.connect(self._suggest_monster_names)
        self._view.btn_refine_description.clicked.connect(self._refine_description)
        self._view.btn_suggest_creature_type.clicked.connect(
            self._suggest_creature_type
        )
        self._view.btn_suggest_alignment.clicked.connect(self._suggest_alignment)
        self._view.btn_suggest_size.clicked.connect(self._suggest_size)
        self._view.btn_generate_artwork.clicked.connect(self._generate_artwork)
        self._view.btn_skills_proficient.clicked.connect(
            partial(self._add_skill, Proficiency.PROFICIENT)
        )
        self._view.btn_skills_expert.clicked.connect(
            partial(self._add_skill, Proficiency.EXPERTISE)
        )
        self._view.btn_skills_remove.clicked.connect(self._remove_skill)
        self._view.btn_damage_resistant.clicked.connect(
            partial(self._add_damage, Resistance.RESISTANT)
        )
        self._view.btn_damage_immune.clicked.connect(
            partial(self._add_damage, Resistance.IMMUNE)
        )
        self._view.btn_damage_remove.clicked.connect(self._remove_damage)
        self._view.btn_languages_add.clicked.connect(self._add_language)
        self._view.btn_languages_remove.clicked.connect(self._remove_language)
        self._view.btn_senses_add.clicked.connect(self._add_sense)
        self._view.btn_senses_remove.clicked.connect(self._remove_sense)
        self._view.btn_conditions_immune.clicked.connect(self._add_condition_immunity)
        self._view.btn_conditions_remove.clicked.connect(
            self._remove_condition_immunity
        )
        self._view.btn_suggest_ability_scores.clicked.connect(
            self._suggest_ability_scores
        )
        self._view.btn_suggest_all.clicked.connect(self._generate_all)
        self._view.btn_generate_markdown.clicked.connect(self.generate_markdown_file)
        self._view.btn_import.clicked.connect(self._import_monster)
        self._view.btn_export.clicked.connect(self._export_monster)
        # Checkbox actions
        self._view.checkbox_has_lair.clicked.connect(self._calc_cr)
        self._view.checkbox_tie_ac_to_cr.clicked.connect(self._toggle_ac_cr_tie)
        self._view.checkbox_tie_hp_to_cr.clicked.connect(self._toggle_hp_cr_tie)
        self._view.checkbox_telepathy.clicked.connect(self._telepathy_toggled)
        self._view.checkbox_prof_st_str.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.STRENGTH)
        )
        self._view.checkbox_prof_st_dex.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.DEXTERITY)
        )
        self._view.checkbox_prof_st_con.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.CONSTITUTION)
        )
        self._view.checkbox_prof_st_int.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.INTELLIGENCE)
        )
        self._view.checkbox_prof_st_wis.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.WISDOM)
        )
        self._view.checkbox_prof_st_cha.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.CHARISMA)
        )
        # Lineedit actions
        self._view.lineedit_name.textChanged.connect(self._name_changed)
        self._view.lineedit_hp.textChanged.connect(self._hp_changed)
        # Textedit actions
        self._view.textedit_description.textChanged.connect(self._description_changed)

    def _ac_changed(self, new_value: int) -> None:
        if self.monster.ac_tied_to_cr:
            return
        self.monster.ac = new_value

    def _hp_changed(self, new_value: str) -> None:
        if self.monster.hp_tied_to_cr:
            return
        self.monster.hp = new_value

    def _creature_type_changed(self, new_type: str) -> None:
        self.monster.creature_type = CreatureType.from_display_name(new_type)
        print(f"Creature type updated to {new_type}")

    def _saving_throw_proficiency_toggled(
        self, ability: Ability, is_proficient: bool
    ) -> None:
        self.monster.saving_throws[ability] = (
            Proficiency.PROFICIENT if is_proficient else Proficiency.NORMAL
        )
        print(
            f"Saving throw proficiency toggled ({ability.display_name} - {is_proficient})"
        )

    def _speed_changed(self, stype: SpeedType, new_speed: int) -> None:
        self.monster.speed[stype] = new_speed
        print(f"Speed type {stype.display_name} updated to {new_speed} ft.")

    def _ability_score_changed(self, ability: Ability, new_value: int) -> None:
        self.monster.ability_scores.scores[ability] = new_value
        print(f"{ability.display_name} updated to {new_value}")

    def _size_changed(self, new_size: str) -> None:
        self.monster.size = Size.from_display_name(new_size)
        print(f"Size updated to {new_size}")

    def _alignment_changed(self, new_alignment: str) -> None:
        self.monster.alignment = Alignment.from_display_name(new_alignment)
        print(f"Alignment updated to {new_alignment}")

    def _name_changed(self, new_name: str) -> None:
        self.monster.name = new_name
        print(f"Name updated to {new_name}")

    def _description_changed(self) -> None:
        self.monster.description = self._view.textedit_description.toPlainText()
        print(f"Description updated to: {self.monster.description}")

    def _telepathy_toggled(self, enabled: bool) -> None:
        self._view.spinbox_telepathy_range.setEnabled(enabled)
        if enabled:
            self.monster.telepathy = (True, self._view.spinbox_telepathy_range.value())
        else:
            self.monster.telepathy = None
        print(f"Telepathy is now {'enabled' if enabled else 'disabled'}")

    def _telepathy_range_changed(self, value: int) -> None:
        self.monster.telepathy = (True, value)
        print(f"Telepathy range updated to {value} ft.")

    def _toggle_ac_cr_tie(self, tie_ac_to_cr: bool) -> None:
        self.monster.ac_tied_to_cr = tie_ac_to_cr
        self._view.spinbox_ac.setEnabled(not self.monster.ac_tied_to_cr)
        if self.monster.ac is not None:
            self._view.spinbox_ac.setValue(self.monster.ac)

    def _toggle_hp_cr_tie(self, tie_hp_to_cr: bool) -> None:
        self.monster.hp_tied_to_cr = tie_hp_to_cr
        self._view.lineedit_hp.setEnabled(not self.monster.hp_tied_to_cr)
        if self.monster.hp is not None:
            self._view.lineedit_hp.setText(self.monster.hp)

    def _calc_cr(self, *args) -> None:
        encounter_size = self._view.cb_encounter_size.currentText()
        if not encounter_size:
            return
        encounter_difficulty = self._view.cb_encounter_difficulty.currentText()
        if not encounter_difficulty:
            return
        avg_party_level = self._view.spinbox_avg_party_level.value()
        if not avg_party_level:
            return
        num_pcs = self._view.spinbox_num_pcs.value()
        if not num_pcs:
            return
        self.encounter = Encounter(
            size=EncounterSize.from_display_name(encounter_size),
            difficulty=EncounterDifficulty.from_display_name(encounter_difficulty),
            num_pcs=num_pcs,
            avg_party_level=avg_party_level,
        )
        self._view.lineedit_challenge_rating.setText(str(self.encounter.monster_cr))
        self.monster.challenge_rating = ChallengeRating(
            self.encounter.monster_cr,
            self._view.checkbox_has_lair.isChecked() == Qt.CheckState.Checked,
        )
        self._view._lbl_per_monster_for_x_monsters.setText(
            f"per monster, for {self.encounter.num_monsters} monsters"
        )
        if self._view.checkbox_tie_ac_to_cr.isChecked():
            self._view.spinbox_ac.setValue(self.monster.challenge_rating.armor_class)
        if (
            self._view.checkbox_tie_hp_to_cr.isChecked()
            and self.monster.ability_scores is not None
            and self._view.cb_size.currentIndex() != -1
        ):
            self._view.lineedit_hp.setText(
                self.monster.challenge_rating.hit_points(
                    self.monster.ability_scores,
                    Size.from_display_name(self._view.cb_size.currentText()),
                )
            )

    def _import_monster(self) -> None:
        pass  # TODO: Implement me

    def _export_monster(self) -> None:
        pass  # TODO: Implement me

    def _generate_all(self) -> None:
        if not self.monster.description:
            print("Can't generate monster without a description. Aborting...")
            return
        if not self.monster.name:
            self._suggest_monster_names()
        self._suggest_creature_type()
        self._suggest_alignment()
        self._suggest_size()
        self._suggest_encounter()
        self._calc_cr()
        self._suggest_ability_scores()
        self._generate_artwork()
        # self._suggest_skill_proficiencies()
        # self._suggest_damage_resistances()
        # self._suggest_condition_immunities()
        # self._suggest_languages()
        # self._suggest_speed()

    def _refine_description(self) -> None:
        print("Refining monster concept...")
        if not self.monster.description:
            if not self.monster.name:
                print("Cannot generate description without a name, skipping...")
                return
            print("Description not found, generating one based on the name...")
            generated_concept = self._mm._openai_agent.generate_text(
                f"Given the following D&D 5E 2024 monster name, generate a 2-3 sentence creative and unique description of that monster. Your response must be that description and no other text whatsoever. The monster's name is: {self.monster.name}"
            )
            print(f"Generated: {generated_concept}")
            self._view.textedit_description.setText(generated_concept)
            return
        refined_concept = self._mm.refine_monster_concept(self.monster.description)
        print(f"Refined: {refined_concept}")
        self._view.textedit_description.setText(refined_concept)

    def _suggest_monster_names(self) -> None:
        print("Suggesting names...")
        suggested_names = self._mm.suggest_names(self.monster.description)
        name = suggested_names[randint(0, len(suggested_names) - 1)].strip(", ")
        self._view.lineedit_name.setText(name)

    def _suggest_creature_type(self) -> None:
        if self.monster.name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.monster.description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting creature type...")
        suggested_creature_type = self._mm._openai_agent.generate_text(
            f"Given the provided D&D monster name and description, suggest an appropriate creature type for it. Your response must be one of the following creature types and nothing else: {', '.join(mt.display_name for mt in CreatureType)}. The name of the monster is: {self.monster.name}. The description of the monster is: {self.monster.description}"
        )
        suggested_monster_type = CreatureType.from_display_name(suggested_creature_type)
        print(f"Suggested Monster Type is: {suggested_monster_type.display_name}")
        suggestion_idx = next(
            (
                i
                for i in range(self._view.cb_creature_type.count())
                if self._view.cb_creature_type.itemText(i)
                == suggested_monster_type.display_name
            )
        )
        self._view.cb_creature_type.setCurrentIndex(suggestion_idx)

    def _suggest_alignment(self) -> None:
        if self.monster.name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.monster.description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting alignment...")
        suggested_alignment = self._mm._openai_agent.generate_text(
            f"Given the provided D&D monster name and description, suggest an appropriate alignment for it. Your response must be one of the following alignments and nothing else: {', '.join([a.display_name for a in Alignment])}. The name of the monster is: {self.monster.name}. The description of the monster is: {self.monster.description}"
        )
        suggested_alignment_enum = Alignment.from_display_name(suggested_alignment)
        print(f"Suggested Alignment is: {suggested_alignment_enum.display_name}")
        suggestion_idx = next(
            (
                i
                for i in range(self._view.cb_alignment.count())
                if self._view.cb_alignment.itemText(i)
                == suggested_alignment_enum.display_name
            )
        )
        self._view.cb_alignment.setCurrentIndex(suggestion_idx)

    def _suggest_size(self) -> None:
        if self.monster.name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.monster.description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting size...")
        suggested_size_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name and description, suggest an appropriate size for it. Your response must be one of the following sizes and nothing else: {', '.join([s.display_name for s in Size])}. The name of the monster is: {self.monster.name}. The description of the monster is: {self.monster.description}"
        )
        suggested_size = Size.from_display_name(suggested_size_txt)
        print(f"Suggested Size is: {suggested_size.display_name}")
        suggestion_idx = next(
            (
                i
                for i in range(self._view.cb_size.count())
                if self._view.cb_size.itemText(i) == suggested_size.display_name
            )
        )
        self._view.cb_size.setCurrentIndex(suggestion_idx)
        self._calc_cr()

    def _suggest_ability_scores(self) -> None:
        if not self.monster.name:
            print("Monster name required to generate ability scores.")
            return
        if not self.monster.description:
            print("Monster description required to generate ability scores.")
            return
        if not self.monster.challenge_rating:
            print("Monster challenge rating required to generate ability scores")
            return
        suggested_scores_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name, description and challenge rating, suggest a set of ability scores for it. Your response must include key-value pairs of the form SCORE_NAME:SCORE_VALUE where SCORE_NAME is Strength,Dexterity,Constitution,Intelligence,Wisdom or Charisma, and SCORE_VALUE is any number 0-30. You must generate one key-value pair for each SCORE_NAME, and no other text whatsoever. The monster's name is: {self.monster.name}. The Monster's Challenge Rating is: {self.monster.challenge_rating.rating}. The Monster's description is: {self.monster.description}."
        )
        suggested_score_lines = [
            sl.replace(" ", "") for sl in suggested_scores_txt.split("\n")
        ]
        suggested_scores = {}
        for sl in suggested_score_lines:
            split = sl.split(":")
            suggested_scores[Ability.from_display_name(split[0])] = int(split[1])
        ab_sc = AbilityScores(suggested_scores)
        self._view.spinbox_str.setValue(ab_sc.scores[Ability.STRENGTH])
        self._view.spinbox_dex.setValue(ab_sc.scores[Ability.DEXTERITY])
        self._view.spinbox_con.setValue(ab_sc.scores[Ability.CONSTITUTION])
        self._view.spinbox_int.setValue(ab_sc.scores[Ability.INTELLIGENCE])
        self._view.spinbox_wis.setValue(ab_sc.scores[Ability.WISDOM])
        self._view.spinbox_cha.setValue(ab_sc.scores[Ability.CHARISMA])

    def _suggest_encounter(self) -> None:
        if not self.monster.name:
            print("Monster name required to generate ability scores.")
            return
        if not self.monster.description:
            print("Monster description required to generate ability scores.")
            return
        print("Suggesting encounter statistics...")
        suggested_encounter_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name and description, suggest appropriate encounter statistics for it. Your response must include key-value pairs of the form KEY:VALUE where KEY is Size,Difficulty,Number of Player Characters and Average Party Level. For the Key 'Size', the valid values are SINGLETON, SMALL, MEDIUM LARGE, SWARM. For the key 'Difficulty', the valid values are LOW, MODERATE and HIGH. For the key 'Number of Player Characters', the valid values are an integer 1-8. For the key 'Average Party Level', the valid values are an integer 1-20. You must generate 1 key-value pair for each KEY, and no other text whatsoever. The monster's name is: {self.monster.name}. The monster's description is: {self.monster.description}"
        )
        suggested_encounter_lines = [
            el.replace(" ", "") for el in suggested_encounter_txt.split("\n")
        ]
        suggested_encounter_size = next(
            (l for l in suggested_encounter_lines if "size:" in l.lower())
        )
        suggested_encounter_size = EncounterSize.from_name(
            suggested_encounter_size.split(":")[1]
        )
        suggested_encounter_difficulty = next(
            (l for l in suggested_encounter_lines if "difficulty:" in l.lower())
        )
        suggested_encounter_difficulty = EncounterDifficulty.from_name(
            suggested_encounter_difficulty.split(":")[1]
        )
        suggested_num_pcs = next(
            (
                l
                for l in suggested_encounter_lines
                if "numberofplayercharacters:" in l.lower()
            )
        )
        suggested_num_pcs = int(suggested_num_pcs.split(":")[1])
        suggested_avg_party_level = next(
            (l for l in suggested_encounter_lines if "averagepartylevel:" in l.lower())
        )
        suggested_avg_party_level = int(suggested_avg_party_level.split(":")[1])
        idx = next(
            (
                i
                for i in range(self._view.cb_encounter_size.count())
                if self._view.cb_encounter_size.itemText(i)
                == str(suggested_encounter_size.display_name)
            )
        )
        self._view.cb_encounter_size.setCurrentIndex(idx)
        print(f"Suggested encounter size: {suggested_encounter_size.display_name}")
        idx = next(
            (
                i
                for i in range(self._view.cb_encounter_difficulty.count())
                if self._view.cb_encounter_difficulty.itemText(i)
                == str(suggested_encounter_difficulty.display_name)
            )
        )
        self._view.cb_encounter_difficulty.setCurrentIndex(idx)
        print(
            f"Suggested encounter difficulty: {suggested_encounter_difficulty.display_name}"
        )
        self._view.spinbox_num_pcs.setValue(suggested_num_pcs)
        print(f"Suggested number of player characters: {suggested_num_pcs}")
        self._view.spinbox_avg_party_level.setValue(suggested_avg_party_level)
        print(f"Suggested average party level: {suggested_avg_party_level}")

    def _add_skill(self, proficiency_level: Proficiency) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        self.monster.skills[skill] = proficiency_level
        if any(
            (
                self._view.listwidget_skills.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(skill.display_name)
                for i in range(self._view.listwidget_skills.count())
            )
        ):
            print(
                f'"{skill.display_name} ({proficiency_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listwidget_skills.addItem(
            f"{skill.display_name} ({proficiency_level.display_name})"
        )

    def _remove_skill(self) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        if skill in self.monster.skills:
            self.monster.skills.pop(skill)
        idx_to_remove = None
        for i in range(self._view.listwidget_skills.count()):
            item_text: str = self._view.listwidget_skills.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(skill.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{skill.display_name}", skipping...')
            return
        self._view.listwidget_skills.takeItem(idx_to_remove)

    def _add_language(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        if language not in self.monster.languages:
            self.monster.languages.append(language)
        if any(
            (
                self._view.listwidget_languages.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(language.display_name)
                for i in range(self._view.listwidget_languages.count())
            )
        ):
            print(f'"{language.display_name}" already exists, not adding duplicate...')
            return
        self._view.listwidget_languages.addItem(language.display_name)

    def _remove_language(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        if language in self.monster.languages:
            self.monster.languages.remove(language)
        idx_to_remove = None
        for i in range(self._view.listwidget_languages.count()):
            item_text: str = self._view.listwidget_languages.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(language.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{language.display_name}", skipping...')
            return
        self._view.listwidget_languages.takeItem(idx_to_remove)

    def _add_damage(self, resistance_level: Resistance) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        self.monster.damage_resistances[dmg_type] = resistance_level
        if any(
            (
                self._view.listwidget_damage.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(dmg_type.display_name)
                for i in range(self._view.listwidget_damage.count())
            )
        ):
            print(
                f'"{dmg_type.display_name} ({resistance_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listwidget_damage.addItem(
            f"{dmg_type.display_name} ({resistance_level.display_name})"
        )

    def _remove_damage(self) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        if dmg_type in self.monster.damage_resistances:
            self.monster.damage_resistances.pop(dmg_type)
        idx_to_remove = None
        for i in range(self._view.listwidget_damage.count()):
            item_text: str = self._view.listwidget_damage.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(dmg_type.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{dmg_type.display_name}", skipping...')
            return
        self._view.listwidget_damage.takeItem(idx_to_remove)

    def _add_sense(self) -> None:
        sense_text = self._view.cb_senses.currentText()
        sense = Sense.from_display_name(sense_text)
        if any(
            (
                self._view.listwidget_senses.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(sense.display_name)
                for i in range(self._view.listwidget_senses.count())
            )
        ):
            print(f'"{sense.display_name}" already exists, not adding duplicate...')
            return
        if self._view.spinbox_sense_range.value() <= 0:
            print(f"Invalid value for sense range, skipping...")
            return
        self.monster.senses[sense] = self._view.spinbox_sense_range.value()
        self._view.listwidget_senses.addItem(
            f"{sense.display_name} - {self._view.spinbox_sense_range.value()}"
        )

    def _remove_sense(self) -> None:
        sense_text = self._view.cb_senses.currentText()
        sense = Sense.from_display_name(sense_text)
        if sense in self.monster.senses:
            self.monster.senses.pop(sense)
        idx_to_remove = None
        for i in range(self._view.listwidget_senses.count()):
            item_text: str = self._view.listwidget_senses.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(sense.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{sense.display_name}", skipping...')
            return
        self._view.listwidget_senses.takeItem(idx_to_remove)

    def _add_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        self.monster.condition_resistances[condition] = Resistance.IMMUNE
        if any(
            (
                self._view.listwidget_conditions.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(condition.display_name)
                for i in range(self._view.listwidget_conditions.count())
            )
        ):
            print(f'"{condition.display_name}" already exists, not adding duplicate...')
            return
        self._view.listwidget_conditions.addItem(f"{condition.display_name}")

    def _remove_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        if condition in self.monster.condition_resistances:
            self.monster.condition_resistances.pop(condition)
        idx_to_remove = None
        for i in range(self._view.listwidget_conditions.count()):
            item_text: str = self._view.listwidget_conditions.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(condition.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{condition.display_name}", skipping...')
            return
        self._view.listwidget_conditions.takeItem(idx_to_remove)

    def _generate_artwork(self) -> None:
        print("Generating artwork...")
        if not self.monster.name:
            print("No name available, skipping")
            return
        if not self.monster.description:
            print("No description available, skipping")
            return
        img_download_filepath = self._output_folder / f"{self.monster.name}_artwork.png"
        revised_prompt, generated_img_url = self._mm._openai_agent.generate_image(
            f"Generate artwork based on the description I will provide below while adhering to the following constraints: 1. The artwork must utilize the art style of the 2024 Dungeons & Dragons Monster Manual (fantasy realism). 2. The artwork must depict the entire body of the creature, without any part of it cropped out of the frame. 3. The artwork must have a plain white background. 4. The artwork must not have any text on it whatsoever. The description to use as inspiration for the art is as follows: {self.monster.description}",
            download_image_to_file=True,
            download_filepath=img_download_filepath,
        )
        print(f"Used the following prompt to generate image: {revised_prompt}")
        print(f"Downloaded image to: {generated_img_url}")
        # Load artwork into label
        pixmap = QPixmap(str(img_download_filepath.resolve()))
        self._view.lbl_artwork.setScaledContents(True)
        self._view.lbl_artwork.resize(500, 500)
        self._view.lbl_artwork.setPixmap(pixmap)

    def generate_markdown_file(
        self,
        checked: bool,
        output_path: Path | None = None,
        wide_statblock: bool = False,
    ) -> None:
        if output_path is None:
            fn = f"{self.monster.name.lower().replace(' ', '_')}_statblock.md"
            output_filepath = self._output_folder / fn
            if not self._output_folder.exists():
                os.makedirs(self._output_folder, exist_ok=True)
        elif not output_path.exists():
            os.makedirs(output_path, exist_ok=True)
        with open(output_filepath, "w") as markdown_file:
            markdown_txt = self.monster.as_homebrewery_v3_markdown(
                wide_statblock=wide_statblock
            )
            markdown_file.write(markdown_txt)
        print(f"File write complete: {output_path}")


# TODO: Traits, Actions, Bonus Actions, Reactions, Legendary Actions, toggle for "has lair", tags, telepathy in the languages display etc.
