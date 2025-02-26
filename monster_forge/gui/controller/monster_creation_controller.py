from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, Qt
import os
from monster_forge.gui.view.create_monster_view import Ui_CreateMonsterView
from monster_forge.monster_maker import MonsterMaker
from monster_forge.dnd.enums import (
    Alignment,
    Skill,
    Language,
    Condition,
    CreatureType,
    Size,
    DamageType,
    Proficiency,
    Resistance,
    Ability,
    SpeedType,
    Sense,
)
from monster_forge.dnd.encounter import Encounter, EncounterDifficulty, EncounterSize
from monster_forge.dnd.challenge_rating import ChallengeRating
from monster_forge.dnd.ability_scores import AbilityScores
from monster_forge.dnd.monster import Monster
from monster_forge.gui.controller.combat_characteristic_controller import (
    CombatCharacteristicController,
)
from pathlib import Path
from functools import partial
from random import randint
import jsonpickle
from monster_forge.pickled_data import PickledMonsterData
from monster_forge.dnd.action import (
    get_all_templates,
    Action,
    BonusAction,
    Reaction,
    LegendaryAction,
    CombatCharacteristic,
    CharacteristicType,
    Trait,
)

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
        self._cc_controllers: dict[str, CombatCharacteristicController] = {}
        self._output_folder: Path = (
            Path(__file__).parent.parent.parent.parent / "generated_output"
        )

    def _setup_UI(self) -> None:
        # Title
        self.setWindowTitle("Create New Monster")
        # AI generation progress bar
        self._view.progressbar_ai_query.setVisible(
            False
        )  # TODO: Make this functional when we query AI
        # Monster name
        self._view.lineedit_name.textChanged.connect(self._name_changed)
        self._view.btn_suggest_name.clicked.connect(self._suggest_monster_names)
        # Monster description
        self._view.textedit_description.textChanged.connect(self._description_changed)
        self._view.btn_refine_description.clicked.connect(self._refine_description)
        # AI "Generate all" button
        self._view.btn_suggest_all.clicked.connect(self._generate_all)
        # Encounter details tab
        self._configure_encounter_tab()
        # General Info tab
        self._configure_general_info_tab()
        # Ability Scores tab
        self._configure_ability_scores_tab()
        # Speed tab
        self._configure_speed_tab()
        # Senses, Languages, Immunities, etc. tab
        self._configure_senses_languages_immunities_tab()
        # Traits, Actions, Bonus Actions, etc. tab
        self._configure_traits_actions_tab()
        # Artwork tab
        self._configure_artwork_tab()
        # Import, Export and Generate Markdown buttons
        self._view.btn_import.clicked.connect(self._import_monster)
        self._view.btn_export.clicked.connect(self._export_monster)
        self._view.btn_generate_markdown.clicked.connect(self.generate_markdown_file)

    def _configure_encounter_tab(self) -> None:
        # Has Lair
        self._view.checkbox_has_lair.clicked.connect(self._calc_cr)
        # Encounter Size
        self._view.cb_encounter_size.addItems(
            sorted([size.display_name for size in EncounterSize])
        )
        self._view.cb_encounter_size.setCurrentIndex(-1)
        self._view.cb_encounter_size.currentIndexChanged.connect(self._calc_cr)
        # Encounter Difficulty
        self._view.cb_encounter_difficulty.addItems(
            sorted([diff.display_name for diff in EncounterDifficulty])
        )
        self._view.cb_encounter_difficulty.setCurrentIndex(-1)
        self._view.cb_encounter_difficulty.currentIndexChanged.connect(self._calc_cr)
        # Average Party Level
        self._view.spinbox_avg_party_level.valueChanged.connect(self._calc_cr)
        # Number of Player Characters
        self._view.spinbox_num_pcs.valueChanged.connect(self._calc_cr)

    def _configure_general_info_tab(self) -> None:
        # Creature Type
        self._view.cb_creature_type.addItems(
            sorted([mt.display_name for mt in CreatureType])
        )
        self._view.cb_creature_type.setCurrentIndex(-1)
        self._view.cb_creature_type.currentTextChanged.connect(
            self._creature_type_changed
        )
        self._view.btn_suggest_creature_type.clicked.connect(
            self._suggest_creature_type
        )
        # Alignment
        self._view.cb_alignment.addItems(
            sorted([alignment.display_name for alignment in Alignment])
        )
        self._view.cb_alignment.setCurrentIndex(-1)
        self._view.cb_alignment.currentTextChanged.connect(self._alignment_changed)
        self._view.btn_suggest_alignment.clicked.connect(self._suggest_alignment)
        # Size
        self._view.cb_size.addItems(sorted([s.display_name for s in Size]))
        self._view.cb_size.setCurrentIndex(-1)
        self._view.cb_size.currentTextChanged.connect(self._size_changed)
        self._view.cb_size.currentIndexChanged.connect(self._calc_cr)
        self._view.btn_suggest_size.clicked.connect(self._suggest_size)
        # Challenge Rating
        self._view.lineedit_challenge_rating.setEnabled(False)
        # AC
        self._view.spinbox_ac.valueChanged.connect(self._ac_changed)
        self._view.checkbox_tie_ac_to_cr.clicked.connect(self._toggle_ac_cr_tie)
        # HP
        self._view.lineedit_hp.textChanged.connect(self._hp_changed)
        self._view.checkbox_tie_hp_to_cr.clicked.connect(self._toggle_hp_cr_tie)

    def _configure_speed_tab(self) -> None:
        # Walk speed
        self._view.spinbox_walk_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.WALKING)
        )
        # Swim speed
        self._view.spinbox_swim_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.SWIM)
        )
        # Fly speed
        self._view.spinbox_fly_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.FLY)
        )
        # Climb speed
        self._view.spinbox_climb_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.CLIMB)
        )
        # Burrow speed
        self._view.spinbox_burrow_speed.valueChanged.connect(
            partial(self._speed_changed, SpeedType.BURROW)
        )

    def _configure_ability_scores_tab(self) -> None:
        # AI Generation button
        self._view.btn_suggest_ability_scores.clicked.connect(
            self._suggest_ability_scores
        )
        # Strength
        self._view.spinbox_str.valueChanged.connect(
            partial(self._ability_score_changed, Ability.STRENGTH)
        )
        self._view.checkbox_prof_st_str.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.STRENGTH)
        )
        # Dexterity
        self._view.spinbox_dex.valueChanged.connect(
            partial(self._ability_score_changed, Ability.DEXTERITY)
        )
        self._view.checkbox_prof_st_dex.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.DEXTERITY)
        )
        # Constitution
        self._view.spinbox_con.valueChanged.connect(
            partial(self._ability_score_changed, Ability.CONSTITUTION)
        )
        self._view.checkbox_prof_st_con.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.CONSTITUTION)
        )
        # Intelligence
        self._view.spinbox_int.valueChanged.connect(
            partial(self._ability_score_changed, Ability.INTELLIGENCE)
        )
        self._view.checkbox_prof_st_int.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.INTELLIGENCE)
        )
        # Wisdom
        self._view.spinbox_wis.valueChanged.connect(
            partial(self._ability_score_changed, Ability.WISDOM)
        )
        self._view.checkbox_prof_st_wis.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.WISDOM)
        )
        # Charisma
        self._view.spinbox_cha.valueChanged.connect(
            partial(self._ability_score_changed, Ability.CHARISMA)
        )
        self._view.checkbox_prof_st_cha.clicked.connect(
            partial(self._saving_throw_proficiency_toggled, Ability.CHARISMA)
        )

    def _configure_senses_languages_immunities_tab(self) -> None:
        # Skill proficiencies
        self._view.cb_skills.addItems(sorted([s.display_name for s in Skill]))
        self._view.cb_skills.setCurrentIndex(-1)
        self._view.btn_skills_proficient.clicked.connect(
            partial(self._btn_add_skill_pressed, Proficiency.PROFICIENT)
        )
        self._view.btn_skills_expert.clicked.connect(
            partial(self._btn_add_skill_pressed, Proficiency.EXPERTISE)
        )
        self._view.btn_skills_remove.clicked.connect(self._btn_remove_skill_pressed)
        # Damage resistances & immunities
        self._view.cb_damage.addItems(sorted([d.display_name for d in DamageType]))
        self._view.cb_damage.setCurrentIndex(-1)
        self._view.btn_damage_resistant.clicked.connect(
            partial(self._btn_add_damage_pressed, Resistance.RESISTANT)
        )
        self._view.btn_damage_immune.clicked.connect(
            partial(self._btn_add_damage_pressed, Resistance.IMMUNE)
        )
        self._view.btn_damage_remove.clicked.connect(self._btn_remove_damage_pressed)
        # Condition immunities
        self._view.cb_conditions.addItems(
            sorted([condition.display_name for condition in Condition])
        )
        self._view.cb_conditions.setCurrentIndex(-1)
        self._view.btn_conditions_immune.clicked.connect(
            self._btn_add_condition_immunity_pressed
        )
        self._view.btn_conditions_remove.clicked.connect(
            self._btn_remove_condition_immunity_pressed
        )
        # Senses
        self._view.cb_senses.addItems(sorted([s.display_name for s in Sense]))
        self._view.cb_senses.setCurrentIndex(-1)
        self._view.btn_senses_add.clicked.connect(self._btn_add_sense_pressed)
        self._view.btn_senses_remove.clicked.connect(self._btn_remove_sense_pressed)
        # Languages
        language_items = []
        for l in Language:
            language_items.append(l.display_name)
            if l.plus_amt > 0:
                items_to_Add = [l.display_name_plus_x(i) for i in range(1, l.plus_amt)]
                language_items.extend(items_to_Add)
        language_items.append("All")
        self._view.cb_languages.addItems(sorted(language_items))
        self._view.cb_languages.setCurrentIndex(-1)
        self._view.btn_languages_add.clicked.connect(self._btn_add_language_pressed)
        self._view.btn_languages_remove.clicked.connect(
            self._btn_remove_language_pressed
        )
        # Telepathy
        self._view.checkbox_telepathy.clicked.connect(self._telepathy_toggled)
        self._view.spinbox_telepathy_range.valueChanged.connect(
            self._telepathy_range_changed
        )

    def _configure_traits_actions_tab(self) -> None:
        # Some data for combobox population
        self._all_templates = get_all_templates()
        # Action presets
        self._view.cb_action_presets.addItems(list(self._all_templates.keys()))
        self._view.btn_use_action_preset.clicked.connect(
            self._btn_use_action_preset_clicked
        )
        # Create Trait
        self._view.btn_create_trait.clicked.connect(self._btn_create_trait_clicked)
        # Create Action
        self._view.btn_create_action.clicked.connect(self._btn_create_action_clicked)
        # Create Bonus Action
        self._view.btn_create_bonus_action.clicked.connect(
            self._btn_create_bonus_action_clicked
        )
        # Create Reaction
        self._view.btn_create_reaction.clicked.connect(
            self._btn_create_reaction_clicked
        )
        # Create Legendary Action
        self._view.btn_create_legendary_action.clicked.connect(
            self._btn_create_legendary_action_clicked
        )

    def _configure_artwork_tab(self) -> None:
        # AI generation button
        self._view.btn_generate_artwork.clicked.connect(self._generate_artwork)

    def _btn_use_action_preset_clicked(self) -> None:
        template_label = self._view.cb_action_presets.currentText()
        if template_label in self._all_templates:
            template = self._all_templates[template_label]
            match template.ctype:
                case CharacteristicType.TRAIT:
                    self._view.lineedit_action_name.setText(template.name)
                    self._view.textedit_action_description.setText(template.description)
                case CharacteristicType.ACTION:
                    self._view.lineedit_action_name.setText(template.name)
                    self._view.textedit_action_description.setText(template.description)
                case CharacteristicType.BONUS_ACTION:
                    self._view.lineedit_action_name.setText(template.name)
                    self._view.textedit_action_description.setText(template.description)
                case CharacteristicType.REACTION:
                    self._view.lineedit_action_name.setText(template.name)
                    self._view.textedit_action_description.setText(template.description)
                case CharacteristicType.LEGENDARY_ACTION:
                    self._view.lineedit_action_name.setText(template.name)
                    self._view.textedit_action_description.setText(template.description)
                case _:
                    raise NotImplementedError

    def _btn_create_action_clicked(self) -> None:
        action_title = self._view.lineedit_action_name.text()
        if not action_title:
            return
        action_description = self._view.textedit_action_description.toPlainText()
        if not action_description:
            return
        if not self.monster.name:
            print("monster name required, skipping...")
            return
        if not self.monster.ability_scores:
            return
        if self.monster.proficiency_bonus is None:
            return
        if not self.monster.saving_throws:
            return
        action = Action(
            self.monster.name,
            self.monster.ability_scores,
            self.monster.proficiency_bonus,
            self.monster.saving_throws,
            self._view.checkbox_has_lair.isChecked(),
            action_title,
            action_description,
        )
        self._add_characteristic(action)
        self._view.lineedit_action_name.clear()
        self._view.textedit_action_description.clear()
        if action.title not in self.monster.actions:
            self.monster.actions[action.title] = action

    def _add_characteristic(self, cc: CombatCharacteristic) -> None:
        ccc = CombatCharacteristicController(cc, parent=self)
        self._cc_controllers[cc.title] = ccc
        ccc.deleted.connect(partial(self._handler_cc_deleted, ccc.cc))
        self._view.tab_actions.layout().addWidget(ccc)

    def _btn_create_bonus_action_clicked(self) -> None:
        bonus_action_title = self._view.lineedit_action_name.text()
        if not bonus_action_title:
            return
        bonus_action_description = self._view.textedit_action_description.toPlainText()
        if not bonus_action_description:
            return
        if not self.monster.name:
            print("monster name required, skipping...")
            return
        if not self.monster.ability_scores:
            return
        if self.monster.proficiency_bonus is None:
            return
        if not self.monster.saving_throws:
            return
        bonus_action = BonusAction(
            self.monster.name,
            self.monster.ability_scores,
            self.monster.proficiency_bonus,
            self.monster.saving_throws,
            self._view.checkbox_has_lair.isChecked(),
            bonus_action_title,
            bonus_action_description,
        )
        self._add_characteristic(bonus_action)
        self._view.lineedit_action_name.clear()
        self._view.textedit_action_description.clear()
        if bonus_action.title not in self.monster.bonus_actions:
            self.monster.bonus_actions[bonus_action.title] = bonus_action

    def _btn_create_reaction_clicked(self) -> None:
        reaction_title = self._view.lineedit_action_name.text()
        if not reaction_title:
            return
        reaction_description = self._view.textedit_action_description.toPlainText()
        if not reaction_description:
            return
        if not self.monster.name:
            print("monster name required, skipping...")
            return
        if not self.monster.ability_scores:
            return
        if self.monster.proficiency_bonus is None:
            return
        if not self.monster.saving_throws:
            return
        reaction = Reaction(
            self.monster.name,
            self.monster.ability_scores,
            self.monster.proficiency_bonus,
            self.monster.saving_throws,
            self._view.checkbox_has_lair.isChecked(),
            reaction_title,
            reaction_description,
        )
        self._add_characteristic(reaction)
        self._view.lineedit_action_name.clear()
        self._view.textedit_action_description.clear()
        if reaction.title not in self.monster.reactions:
            self.monster.reactions[reaction.title] = reaction

    def _btn_create_legendary_action_clicked(self) -> None:
        legendary_action_title = self._view.lineedit_action_name.text()
        if not legendary_action_title:
            return
        legendary_action_description = (
            self._view.textedit_action_description.toPlainText()
        )
        if not legendary_action_description:
            return
        if not self.monster.name:
            print("monster name required, skipping...")
            return
        if not self.monster.ability_scores:
            return
        if self.monster.proficiency_bonus is None:
            return
        if not self.monster.saving_throws:
            return
        legendary_action = LegendaryAction(
            self.monster.name,
            self.monster.ability_scores,
            self.monster.proficiency_bonus,
            self.monster.saving_throws,
            self._view.checkbox_has_lair.isChecked(),
            legendary_action_title,
            legendary_action_description,
        )
        self._add_characteristic(legendary_action)
        self._view.lineedit_action_name.clear()
        self._view.textedit_action_description.clear()
        if legendary_action.title not in self.monster.legendary_actions:
            self.monster.legendary_actions[legendary_action.title] = legendary_action

    def _btn_create_trait_clicked(self) -> None:
        trait_title = self._view.lineedit_action_name.text()
        if not trait_title:
            print("Trait title required, skipping...")
            return
        trait_description = self._view.textedit_action_description.toPlainText()
        if not trait_description:
            print("Trait description required, skipping...")
            return
        if not self.monster.name:
            print("monster name required, skipping...")
            return
        if not self.monster.ability_scores:
            return
        if self.monster.proficiency_bonus is None:
            return
        if not self.monster.saving_throws:
            return
        trait = Trait(
            self.monster.name,
            self.monster.ability_scores,
            self.monster.proficiency_bonus,
            self.monster.saving_throws,
            self._view.checkbox_has_lair.isChecked(),
            trait_title,
            trait_description,
        )
        self._add_characteristic(trait)
        self._view.lineedit_action_name.clear()
        self._view.textedit_action_description.clear()
        if trait.title not in self.monster.traits:
            self.monster.traits[trait.title] = trait

    def _handler_cc_deleted(self, cc: CombatCharacteristic, pop: bool = True) -> None:
        controller = self._cc_controllers.get(cc.title, None)
        if controller is not None:
            self._view.tab_actions.layout().removeWidget(controller)
            controller.deleteLater()
            match cc.ctype:
                case CharacteristicType.TRAIT:
                    if pop:
                        self.monster.traits.pop(cc.title, None)
                case CharacteristicType.ACTION:
                    if pop:
                        self.monster.actions.pop(cc.title, None)
                case CharacteristicType.BONUS_ACTION:
                    if pop:
                        self.monster.bonus_actions.pop(cc.title, None)
                case CharacteristicType.REACTION:
                    if pop:
                        self.monster.reactions.pop(cc.title, None)
                case CharacteristicType.LEGENDARY_ACTION:
                    if pop:
                        self.monster.legendary_actions.pop(cc.title, None)
                case _:
                    raise NotImplementedError
            print(f"Deleted combat characteristic: {cc.title}")
        else:
            print(f"Couldn't find widget for combat characteristic: {cc.title}")

    def _clear_characteristics(self, pop: bool = False) -> None:
        for ccc in self._cc_controllers.values():
            self._handler_cc_deleted(ccc.cc, pop=pop)

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
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Open File",
            str(self._output_folder),
            "Statblock Files (*.statblock.json)",
        )
        if file_path:
            load_successful = False
            with open(file_path, "r") as imported_file:
                data = imported_file.read()
                unpickled_monster: PickledMonsterData = jsonpickle.decode(
                    data, keys=True
                )
                self.monster = unpickled_monster.monster
                self.encounter = unpickled_monster.encounter
                load_successful = True
            if load_successful:
                self._view.lineedit_name.setText(self.monster.name)
                self._view.textedit_description.setText(self.monster.description)
                if self.monster.challenge_rating is not None:
                    self._view.checkbox_has_lair.setChecked(
                        self.monster.challenge_rating.has_lair
                    )
                self._view.cb_encounter_size.blockSignals(True)
                self._view.cb_encounter_difficulty.blockSignals(True)
                self._view.spinbox_avg_party_level.blockSignals(True)
                self._view.spinbox_num_pcs.blockSignals(True)
                idx = next(
                    (
                        i
                        for i in range(self._view.cb_encounter_size.count())
                        if self._view.cb_encounter_size.itemText(i)
                        == self.encounter.size.display_name
                    ),
                    -1,
                )
                self._view.cb_encounter_size.setCurrentIndex(idx)
                idx = next(
                    (
                        i
                        for i in range(self._view.cb_encounter_difficulty.count())
                        if self._view.cb_encounter_difficulty.itemText(i)
                        == self.encounter.difficulty.display_name
                    ),
                    -1,
                )
                self._view.cb_encounter_difficulty.setCurrentIndex(idx)
                self._view.spinbox_avg_party_level.setValue(
                    self.encounter.avg_party_level or 1
                )
                self._view.spinbox_num_pcs.setValue(self.encounter.num_pcs or 1)
                self._view.cb_encounter_size.blockSignals(False)
                self._view.cb_encounter_difficulty.blockSignals(False)
                self._view.spinbox_avg_party_level.blockSignals(False)
                self._view.spinbox_num_pcs.blockSignals(False)
                idx = next(
                    (
                        i
                        for i in range(self._view.cb_creature_type.count())
                        if self._view.cb_creature_type.itemText(i)
                        == self.monster.creature_type.display_name
                    ),
                    -1,
                )
                self._view.cb_creature_type.setCurrentIndex(idx)
                idx = next(
                    (
                        i
                        for i in range(self._view.cb_alignment.count())
                        if self._view.cb_alignment.itemText(i)
                        == self.monster.alignment.display_name
                    ),
                    -1,
                )
                self._view.cb_alignment.setCurrentIndex(idx)
                idx = next(
                    (
                        i
                        for i in range(self._view.cb_size.count())
                        if self._view.cb_size.itemText(i)
                        == self.monster.size.display_name
                    ),
                    -1,
                )
                self._view.cb_size.blockSignals(True)
                self._view.cb_size.setCurrentIndex(idx)
                self._view.cb_size.blockSignals(False)
                self._view.spinbox_walk_speed.setValue(
                    self.monster.speed.get(SpeedType.WALKING, 0)
                )
                self._view.spinbox_swim_speed.setValue(
                    self.monster.speed.get(SpeedType.SWIM, 0)
                )
                self._view.spinbox_climb_speed.setValue(
                    self.monster.speed.get(SpeedType.CLIMB, 0)
                )
                self._view.spinbox_fly_speed.setValue(
                    self.monster.speed.get(SpeedType.FLY, 0)
                )
                self._view.spinbox_burrow_speed.setValue(
                    self.monster.speed.get(SpeedType.BURROW, 0)
                )
                self._view.spinbox_str.setValue(
                    self.monster.ability_scores.scores.get(Ability.STRENGTH, 10)
                )
                self._view.checkbox_prof_st_str.setChecked(
                    self.monster.saving_throws.get(Ability.STRENGTH, Proficiency.NORMAL)
                    == Proficiency.PROFICIENT
                )
                self._view.spinbox_dex.setValue(
                    self.monster.ability_scores.scores.get(Ability.DEXTERITY, 10)
                )
                self._view.checkbox_prof_st_dex.setChecked(
                    self.monster.saving_throws.get(
                        Ability.DEXTERITY, Proficiency.NORMAL
                    )
                    == Proficiency.PROFICIENT
                )
                self._view.spinbox_con.setValue(
                    self.monster.ability_scores.scores.get(Ability.CONSTITUTION, 10)
                )
                self._view.checkbox_prof_st_con.setChecked(
                    self.monster.saving_throws.get(
                        Ability.CONSTITUTION, Proficiency.NORMAL
                    )
                    == Proficiency.PROFICIENT
                )
                self._view.spinbox_int.setValue(
                    self.monster.ability_scores.scores.get(Ability.INTELLIGENCE, 10)
                )
                self._view.checkbox_prof_st_int.setChecked(
                    self.monster.saving_throws.get(
                        Ability.INTELLIGENCE, Proficiency.NORMAL
                    )
                    == Proficiency.PROFICIENT
                )
                self._view.spinbox_wis.setValue(
                    self.monster.ability_scores.scores.get(Ability.WISDOM, 10)
                )
                self._view.checkbox_prof_st_wis.setChecked(
                    self.monster.saving_throws.get(Ability.WISDOM, Proficiency.NORMAL)
                    == Proficiency.PROFICIENT
                )
                self._view.spinbox_cha.setValue(
                    self.monster.ability_scores.scores.get(Ability.CHARISMA, 10)
                )
                self._view.checkbox_prof_st_cha.setChecked(
                    self.monster.saving_throws.get(Ability.CHARISMA, Proficiency.NORMAL)
                    == Proficiency.PROFICIENT
                )
                self._calc_cr()
                self._view.listwidget_skills.clear()
                for skill, prof in self.monster.skills.items():
                    self._add_skill(skill, prof)
                self._view.listwidget_damage.clear()
                for dmg_type, res in self.monster.damage_resistances.items():
                    self._add_damage(dmg_type, res)
                self._view.listwidget_conditions.clear()
                for condition in self.monster.condition_resistances.keys():
                    self._add_condition_immunity(condition)
                self._view.listwidget_senses.clear()
                for sense, range_ft in self.monster.senses.items():
                    self._add_sense(sense, range_ft)
                self._view.listwidget_languages.clear()
                for language in self.monster.languages:
                    self._add_language(language)
                if self.monster.telepathy is not None:
                    self._view.checkbox_telepathy.setChecked(self.monster.telepathy[0])
                    self._view.spinbox_telepathy_range.setValue(
                        self.monster.telepathy[1]
                    )
                    self._view.spinbox_telepathy_range.setEnabled(
                        self.monster.telepathy[0]
                    )
                self._clear_characteristics()
                for action in self.monster.actions.values():
                    self._add_characteristic(action)
                for bonus_action in self.monster.bonus_actions.values():
                    self._add_characteristic(bonus_action)
                for reaction in self.monster.reactions.values():
                    self._add_characteristic(reaction)
                for legendary_action in self.monster.legendary_actions.values():
                    self._add_characteristic(legendary_action)

    def _export_monster(self) -> None:
        pickled_monster_data = PickledMonsterData(self.monster, self.encounter)
        pickled_monster = jsonpickle.encode(pickled_monster_data, keys=True)
        filepath = self._output_folder / f"{self.monster.name}.statblock.json"
        with open(filepath, "w") as export_file:
            export_file.write(pickled_monster)
        print(f"Exported monster ({self.monster.name}) to: {filepath}")

    def _generate_text(self, what_to_generate: str, response_constraints: str) -> str:
        return self._mm._openai_agent.generate_text(
            f"Given the provided information about a new D&D 5E 2024 monster, suggest {what_to_generate}. Your response must be {response_constraints} and have no other text whatsoever. {self.monster.all_available_prompt_info}"
        )

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
        self._suggest_skill_proficiencies()
        self._suggest_damage_resistances()
        self._suggest_condition_immunities()
        self._suggest_languages()
        self._suggest_speed()
        self._suggest_senses()
        self._suggest_telepathy()
        # self._generate_artwork()

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
            f"Given the provided D&D 5E 2024 monster name and description, suggest an appropriate alignment for it. Your response must be one of the following alignments and nothing else: {', '.join([a.display_name for a in Alignment])}. The name of the monster is: {self.monster.name}. The description of the monster is: {self.monster.description}"
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

    def _suggest_skill_proficiencies(self) -> None:
        print("Suggesting skill proficiencies...")
        suggested_skill_proficiencies = self._generate_text(
            "a comma separated list of key:value pairs where the key is a skill and the value is the level of proficiency the creature has in that skill",
            f"a comma separated list of key:value pairs where the key must be one of the following: {', '.join([s.display_name for s in Skill])} and the value must be one of the following: {', '.join(p.display_name for p in Proficiency if p != Proficiency.NORMAL)}",
        )
        print(f"Suggested skill proficiencies are: {suggested_skill_proficiencies}")
        self._view.listwidget_skills.clear()
        for ssp in suggested_skill_proficiencies.split(","):
            split = ssp.strip().split(":")
            skill_text = split[0].strip()
            skill = Skill.from_display_name(skill_text)
            proficiency_text = split[1].strip()
            proficiency = Proficiency.from_display_name(proficiency_text)
            self._add_skill(skill, proficiency)

    def _suggest_damage_resistances(self) -> None:
        print("Suggesting damage resistances and immunities...")
        suggested_damage_resistances = self._generate_text(
            "a comma separated list of key:value pairs where the key is a damage type and the value is the type of resistance the creature has to the damage",
            f"a comma separated list of key:value pairs where the key must be one of the following: {', '.join([dt.display_name for dt in DamageType])} and the value must be one of the following: {', '.join(rt.display_name for rt in Resistance if rt != Resistance.NORMAL)}",
        )
        print(f"Suggested damage resistances are: {suggested_damage_resistances}")
        self._view.listwidget_damage.clear()
        for sdr in suggested_damage_resistances.split(","):
            split = sdr.strip().split(":")
            damage_type_text = split[0].strip()
            damage_type = DamageType.from_display_name(damage_type_text)
            resistance_text = split[1].strip()
            resistance = Resistance.from_display_name(resistance_text)
            self._add_damage(damage_type, resistance)

    def _suggest_senses(self) -> None:
        print("Suggesting senses...")
        suggested_senses = self._generate_text(
            "a comma separated list of key:value pairs where the key is a sense that creature would possess and the value is an integer representing the range in feet of that sense",
            f"a comma separated list of key:value pairs where the key is one of the following options: {', '.join([s.display_name for s in Sense])} and the value is an integer between 0 and 300 and is divisible by 5",
        )
        print(f"Suggested senses are: {suggested_senses}")
        self._view.listwidget_senses.clear()
        for ss in suggested_senses.split(","):
            split = ss.strip().split(":")
            sense_text = split[0].strip()
            sense = Sense.from_display_name(sense_text)
            sense_range = int(split[1].strip())
            if sense_range % 5 != 0 or sense_range <= 0:
                sense_range = 0
            if sense_range > 0:
                self._add_sense(sense, sense_range)

    def _suggest_telepathy(self) -> None:
        print("Suggesting telepathy capabilities...")
        telepathy_suggestion = self._generate_text(
            "a single key:value pair where the key is True or False if the creature has telepathy and the value is the range of that telepathy in feet",
            "a single key:value pair where the key is True if the creature has telepathy and False if it does not, and the value is an integer between 0 and 300 inclusive and is divisible by 5",
        )
        split = telepathy_suggestion.split(":")
        has_telepathy = True if split[0].strip().lower() == "true" else False
        telepathy_range_ft = int(split[1].strip())
        print(f"Suggested telepathy: {has_telepathy} - {telepathy_range_ft} ft.")
        self.monster.telepathy = (has_telepathy, telepathy_range_ft)
        self._view.checkbox_telepathy.setChecked(has_telepathy)
        self._view.spinbox_telepathy_range.setValue(telepathy_range_ft)
        self._view.spinbox_telepathy_range.setEnabled(has_telepathy)

    def _suggest_condition_immunities(self) -> None:
        suggested_condition_immunities = self._generate_text(
            "a comma separated list of conditions that creature would be immune to",
            f"a comma separated list of values from the following options: {', '.join([c.display_name for c in Condition])}",
        )
        print(f"Suggested condition immunities are: {suggested_condition_immunities}")
        condition_immunities = sorted(
            [
                Condition.from_display_name(sc.strip())
                for sc in suggested_condition_immunities.split(",")
                if Condition.is_valid_display_name(sc)
            ],
            key=lambda x: x.display_name.lower(),
        )
        self.monster.condition_resistances = {
            condition: Resistance.IMMUNE for condition in condition_immunities
        }
        self._view.listwidget_conditions.clear()
        for condition in condition_immunities:
            self._add_condition_immunity(condition)

    def _suggest_languages(self) -> None:
        if self.monster.name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.monster.description is None:
            print("Creature does not yet have a description, skipping...")
            return
        print("Suggesting languages...")
        suggested_languages = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name and description, suggest a comma separated list of languages that creature would know. Your response must be a comma separated list of values from the following options: {', '.join([l.display_name for l in Language])} and have no other text whatsoever. The name of the monster is: {self.monster.name}. The description of the monster is: {self.monster.description}"
        )
        print(f"Suggested languages are: {suggested_languages}")
        languages = sorted(
            [
                Language.from_display_name(sl.strip())
                for sl in suggested_languages.split(",")
            ],
            key=lambda x: x.display_name.lower(),
        )
        self.monster.languages.clear()
        self._view.listwidget_languages.clear()
        for language in languages:
            self._add_language(language)

    def _suggest_speed(self) -> None:
        print("Suggesting speed...")
        suggested_speed = self._generate_text(
            "a comma separated list of key:value pairs representing the speed values appropriate for the monster.",
            f"a comma separated list of key:value pairs where the key value is one of the following: {', '.join([st.display_name for st in SpeedType])}, and the values are integers between 0-200 that are divisble by 5",
        )
        print(f"Suggested speeds are: {suggested_speed}")
        ui_cache = {
            SpeedType.WALKING: self._view.spinbox_walk_speed,
            SpeedType.SWIM: self._view.spinbox_swim_speed,
            SpeedType.CLIMB: self._view.spinbox_climb_speed,
            SpeedType.FLY: self._view.spinbox_fly_speed,
            SpeedType.BURROW: self._view.spinbox_burrow_speed,
        }
        self.monster.speed.clear()
        for ss in suggested_speed.split(","):
            split = ss.strip().split(":")
            speed_type_text = split[0]
            speed = SpeedType.from_display_name(speed_type_text)
            speed_range = int(split[1])
            if speed_range % 5 != 0 or speed_range <= 0:
                speed_range = 0
            self.monster.speed[speed] = speed_range
            ui_cache[speed].setValue(speed_range)

    def _add_skill(self, skill: Skill, proficiency_level: Proficiency) -> None:
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

    def _btn_add_skill_pressed(self, proficiency_level: Proficiency) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        self._add_skill(skill, proficiency_level)

    def _remove_skill(self, skill: Skill) -> None:
        if skill in self.monster.skills:
            self.monster.skills.pop(skill)
        idx_to_remove = next(
            (
                i
                for i in range(self._view.listwidget_skills.count())
                if self._view.listwidget_languages.item(i)
                .text()
                .startswith(skill.display_name)
            ),
            None,
        )
        if idx_to_remove is not None:
            self._view.listwidget_skills.takeItem(idx_to_remove)

    def _btn_remove_skill_pressed(self) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        self._remove_skill(skill)

    def _add_language(self, language: Language) -> None:
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
            print("Language already in UI, skipping...")
            return
        self._view.listwidget_languages.addItem(language.display_name)

    def _remove_language(self, language: Language) -> None:
        if language in self.monster.languages:
            self.monster.languages.remove(language)
        idx_to_remove = next(
            (
                i
                for i in range(self._view.listwidget_languages.count())
                if self._view.listwidget_languages.item(i)
                .text()
                .startswith(language.display_name)
            ),
            None,
        )
        if idx_to_remove is not None:
            self._view.listwidget_languages.takeItem(idx_to_remove)

    def _btn_add_language_pressed(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        self._add_language(language)

    def _btn_remove_language_pressed(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        self._remove_language(language)

    def _add_damage(
        self, damage_type: DamageType, resistance_level: Resistance
    ) -> None:
        self.monster.damage_resistances[damage_type] = resistance_level
        if any(
            (
                self._view.listwidget_damage.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(damage_type.display_name)
                for i in range(self._view.listwidget_damage.count())
            )
        ):
            print(
                f'"{damage_type.display_name} ({resistance_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listwidget_damage.addItem(
            f"{damage_type.display_name} ({resistance_level.display_name})"
        )

    def _btn_add_damage_pressed(self, resistance_level: Resistance) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        self._add_damage(dmg_type, resistance_level)

    def _remove_damage(self, damage_type: DamageType) -> None:
        if damage_type in self.monster.damage_resistances:
            self.monster.damage_resistances.pop(damage_type)
        idx_to_remove = next(
            (
                i
                for i in range(self._view.listwidget_damage.count())
                if self._view.listwidget_damage.item(i)
                .text()
                .startswith(damage_type.display_name)
            ),
            None,
        )
        if idx_to_remove is not None:
            self._view.listwidget_damage.takeItem(idx_to_remove)

    def _btn_remove_damage_pressed(self) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        self._remove_damage(dmg_type)

    def _add_sense(self, sense: Sense, range_ft: int) -> None:
        self.monster.senses[sense] = range_ft
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
        self._view.listwidget_senses.addItem(f"{sense.display_name} - {range_ft}")

    def _btn_add_sense_pressed(self) -> None:
        sense_text = self._view.cb_senses.currentText()
        sense = Sense.from_display_name(sense_text)
        if self._view.spinbox_sense_range.value() <= 0:
            print(f"Invalid value for sense range, skipping...")
            return
        self._add_sense(sense, self._view.spinbox_sense_range.value())

    def _remove_sense(self, sense: Sense) -> None:
        if sense in self.monster.senses:
            self.monster.senses.pop(sense)
        idx_to_remove = next(
            (
                i
                for i in range(self._view.listwidget_senses.count())
                if self._view.listwidget_senses.item(i)
                .text()
                .startswith(sense.display_name)
            ),
            None,
        )
        if idx_to_remove is not None:
            self._view.listwidget_senses.takeItem(idx_to_remove)

    def _btn_remove_sense_pressed(self) -> None:
        sense_text = self._view.cb_senses.currentText()
        sense = Sense.from_display_name(sense_text)
        self._remove_sense(sense)

    def _add_condition_immunity(self, condition: Condition) -> None:
        if condition not in self.monster.condition_resistances:
            self.monster.condition_resistances[condition] = Resistance.IMMUNE
        if any(
            (
                self._view.listwidget_conditions.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(condition.display_name)
                for i in range(self._view.listwidget_conditions.count())
            )
        ):
            print("Condition already in UI, skipping...")
            return
        self._view.listwidget_conditions.addItem(condition.display_name)

    def _btn_add_condition_immunity_pressed(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        self._add_condition_immunity(condition)
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

    def _remove_condition_immunity(self, condition: Condition) -> None:
        if condition in self.monster.condition_resistances:
            self.monster.condition_resistances.pop(condition)
        idx_to_remove = next(
            (
                i
                for i in range(self._view.listwidget_conditions.count())
                if self._view.listwidget_conditions.item(i)
                .text()
                .startswith(condition.display_name)
            ),
            None,
        )
        if idx_to_remove is not None:
            self._view.listwidget_conditions.takeItem(idx_to_remove)

    def _btn_remove_condition_immunity_pressed(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        self._remove_condition_immunity(condition)

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
            markdown_txt = self.monster.as_homebrewery_v3_markdown_2024(
                wide_statblock=wide_statblock
            )
            markdown_file.write(markdown_txt)
        print(f"File write complete: {output_path}")


# TODO: Dice roll macros
