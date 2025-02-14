from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from collections.abc import Sequence
from PyQt5.QtCore import QObject, Qt
import re
from monster_forge.gui.view.monster_creation_view import (
    Ui_MonsterCreationView,
)
from monster_forge.monster_maker import MonsterMaker
from monster_forge.dnd.dnd import (
    Alignment,
    EncounterDifficulty,
    EncounterSize,
    Skill,
    Language,
    Condition,
    MonsterType,
    Size,
    DamageType,
    ChallengeRating,
    Encounter,
    Proficiency,
    LanguageProficiency,
    Resistance,
    AbilityScores,
    Ability,
)
from pathlib import Path
from functools import partial

# A demon who disguises itself amongst the cultural and financial elite, attending soirees and other lavish events. It lures in its victims with its impeccable charm and decorum.


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_MonsterCreationView()
        self._view.setupUi(self)
        self._mm = MonsterMaker()
        self._setup_UI()

    def _setup_UI(self) -> None:
        self.setWindowTitle("Create New Monster")
        self._view.progressbar_main.setVisible(False)
        self._view.progressbar_generate_all.setVisible(False)
        self._view.btn_refine_description.clicked.connect(self._refine_description)
        self._view.btn_suggest_names.clicked.connect(self._suggest_monster_names)
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
            sorted([mt.display_name for mt in MonsterType])
        )
        self._view.cb_creature_type.setCurrentIndex(-1)
        self._view.cb_languages.addItems(sorted([l.display_name for l in Language]))
        self._view.cb_languages.setCurrentIndex(-1)
        self._view.cb_size.addItems(sorted([s.display_name for s in Size]))
        self._view.cb_size.setCurrentIndex(-1)
        self._view.cb_damage.addItems(sorted([d.display_name for d in DamageType]))
        self._view.cb_damage.setCurrentIndex(-1)
        self._view.lineedit_challenge_rating.setEnabled(False)
        self._view.cb_encounter_size.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_encounter_difficulty.currentIndexChanged.connect(self._calc_cr)
        self._view.spinbox_avg_party_lvl.valueChanged.connect(self._calc_cr)
        self._view.spinbox_num_pcs.valueChanged.connect(self._calc_cr)
        self._view.btn_generate_artwork.clicked.connect(self._generate_artwork)
        self._view.btn_suggest_creature_type.clicked.connect(
            self._suggest_creature_type
        )
        self._view.btn_suggest_alignment.clicked.connect(self._suggest_alignment)
        self._view.btn_suggest_size.clicked.connect(self._suggest_size)
        self._view.btn_proficient_skill.clicked.connect(
            partial(self._add_skill, Proficiency.PROFICIENT)
        )
        self._view.btn_expert_skill.clicked.connect(
            partial(self._add_skill, Proficiency.EXPERTISE)
        )
        self._view.btn_remove_skill.clicked.connect(self._remove_skill)
        self._view.btn_resistant_damage.clicked.connect(
            partial(self._add_damage, Resistance.RESISTANT)
        )
        self._view.btn_immune_damage.clicked.connect(
            partial(self._add_damage, Resistance.IMMUNE)
        )
        self._view.btn_remove_damage.clicked.connect(self._remove_damage)
        self._view.btn_understands_language.clicked.connect(
            partial(self._add_language, LanguageProficiency.UNDERSTANDS)
        )
        self._view.btn_speaks_language.clicked.connect(
            partial(self._add_language, LanguageProficiency.SPEAKS)
        )
        self._view.btn_remove_language.clicked.connect(self._remove_language)
        self._view.btn_immune_condition.clicked.connect(self._add_condition_immunity)
        self._view.btn_remove_condition.clicked.connect(self._remove_condition_immunity)
        self._view.checkbox_ac_cr_tie.clicked.connect(self._toggle_ac_cr_tie)
        self._view.checkbox_hp_cr_tie.clicked.connect(self._toggle_hp_cr_tie)

    def _toggle_ac_cr_tie(self, tie_ac_to_cr: bool) -> None:
        if tie_ac_to_cr:
            self._view.spinbox_ac.setEnabled(False)
            if self.current_challenge_rating is not None:
                self._view.spinbox_ac.setValue(
                    self.current_challenge_rating.armor_class
                )
        else:
            self._view.spinbox_ac.setEnabled(True)

    def _toggle_hp_cr_tie(self, tie_hp_to_cr: bool) -> None:
        if tie_hp_to_cr:
            self._view.lineedit_hp.setEnabled(False)
            if (
                self.current_size is not None
                and self.current_challenge_rating is not None
            ):
                self._view.lineedit_hp.setText(
                    self.current_challenge_rating.hit_points(
                        self.current_ability_scores, self.current_size
                    )
                )
        else:
            self._view.lineedit_hp.setEnabled(True)

    def _calc_cr(self, *args) -> None:
        if None not in [
            self.current_encounter_size,
            self.current_encounter_difficulty,
            self.current_avg_party_level,
            self.current_num_pcs,
        ]:
            encounter = Encounter(
                self.current_encounter_size,
                self.current_encounter_difficulty,
                num_pcs=self.current_num_pcs,
                avg_party_level=self.current_avg_party_level,
            )
            self._view.lineedit_challenge_rating.setText(str(encounter.monster_cr))
            self._view.lbl_per_monster_for_x_monsters.setText(
                f"per monster, for {encounter.num_monsters} monsters"
            )
            if (
                self.current_challenge_rating is not None
                and self._view.checkbox_ac_cr_tie.isChecked()
            ):
                self._view.spinbox_ac.setValue(
                    self.current_challenge_rating.armor_class
                )
            if (
                self.current_challenge_rating is not None
                and self._view.checkbox_hp_cr_tie.isChecked()
            ):
                if self.current_size is not None:
                    self._view.lineedit_hp.setText(
                        self.current_challenge_rating.hit_points(
                            self.current_ability_scores, self.current_size
                        )
                    )

    def _refine_description(self) -> None:
        print("Refining monster concept...")
        if not self.current_description:
            raise RuntimeError
        refined_concept = self._mm.refine_monster_concept(self.current_description)
        print(f"Refined: {refined_concept}")
        self._view.textedit_description.setText(refined_concept)

    def _suggest_monster_names(self) -> None:
        print("Suggesting names...")
        suggested_names = self._mm.suggest_names(self.current_monster_concept)
        self._view.lineedit_name.setText(", ".join(suggested_names))

    def _suggest_creature_type(self) -> None:
        if self.current_name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.current_description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting creature type...")
        suggested_creature_type = self._mm._openai_agent.generate_text(
            f"Given the provided D&D monster name and description, suggest an appropriate creature type for it. Your response must be one of the following creature types and nothing else: {', '.join(mt.display_name for mt in MonsterType)}. The name of the monster is: {self.current_name}. The description of the monster is: {self.current_description}"
        )
        suggested_monster_type = MonsterType.from_display_name(suggested_creature_type)
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
        if self.current_name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.current_description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting alignment...")
        suggested_alignment = self._mm._openai_agent.generate_text(
            f"Given the provided D&D monster name and description, suggest an appropriate alignment for it. Your response must be one of the following alignments and nothing else: {', '.join([a.display_name for a in Alignment])}. The name of the monster is: {self.current_name}. The description of the monster is: {self.current_description}"
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
        if self.current_name is None:
            print("Creature does not yet have a name, skipping...")
            return
        if self.current_description is None:
            print("Creature does not yet have a description, skippingl...")
            return
        print("Suggesting size...")
        suggested_size_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D monster name and description, suggest an appropriate size for it. Your response must be one of the following sizes and nothing else: {', '.join([s.display_name for s in Size])}. The name of the monster is: {self.current_name}. The description of the monster is: {self.current_description}"
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

    def _add_skill(self, proficiency_level: Proficiency) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        if any(
            (
                self._view.listview_skills.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(skill.display_name)
                for i in range(self._view.listview_skills.count())
            )
        ):
            print(
                f'"{skill.display_name} ({proficiency_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listview_skills.addItem(
            f"{skill.display_name} ({proficiency_level.display_name})"
        )

    def _remove_skill(self) -> None:
        skill_text = self._view.cb_skills.currentText()
        skill = Skill.from_display_name(skill_text)
        idx_to_remove = None
        for i in range(self._view.listview_skills.count()):
            item_text: str = self._view.listview_skills.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(skill.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{skill.display_name}", skipping...')
            return
        self._view.listview_skills.takeItem(idx_to_remove)

    def _add_language(self, proficiency_level: LanguageProficiency) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        if any(
            (
                self._view.listview_languages.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(language.display_name)
                for i in range(self._view.listview_languages.count())
            )
        ):
            print(
                f'"{language.display_name} ({proficiency_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listview_languages.addItem(
            f"{language.display_name} ({proficiency_level.display_name})"
        )

    def _remove_language(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        idx_to_remove = None
        for i in range(self._view.listview_languages.count()):
            item_text: str = self._view.listview_languages.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(language.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{language.display_name}", skipping...')
            return
        self._view.listview_languages.takeItem(idx_to_remove)

    def _add_damage(self, resistance_level: Resistance) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        if any(
            (
                self._view.listview_damage.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(dmg_type.display_name)
                for i in range(self._view.listview_damage.count())
            )
        ):
            print(
                f'"{dmg_type.display_name} ({resistance_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listview_damage.addItem(
            f"{dmg_type.display_name} ({resistance_level.display_name})"
        )

    def _remove_damage(self) -> None:
        dmg_text = self._view.cb_damage.currentText()
        dmg_type = DamageType.from_display_name(dmg_text)
        idx_to_remove = None
        for i in range(self._view.listview_damage.count()):
            item_text: str = self._view.listview_damage.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(dmg_type.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{dmg_type.display_name}", skipping...')
            return
        self._view.listview_damage.takeItem(idx_to_remove)

    def _add_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        if any(
            (
                self._view.listview_conditions.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(condition.display_name)
                for i in range(self._view.listview_conditions.count())
            )
        ):
            print(
                f'"{condition.display_name} ({Resistance.IMMUNE.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listview_conditions.addItem(
            f"{condition.display_name} ({Resistance.IMMUNE.display_name})"
        )

    def _remove_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        idx_to_remove = None
        for i in range(self._view.listview_conditions.count()):
            item_text: str = self._view.listview_conditions.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            if item_text.startswith(condition.display_name):
                idx_to_remove = i
                break
        if idx_to_remove is None:
            print(f'Cannot find index for "{condition.display_name}", skipping...')
            return
        self._view.listview_conditions.takeItem(idx_to_remove)

    def _generate_artwork(self) -> None:
        print("Generating artwork...")
        if not self.current_name:
            print("No name available, skipping")
            return
        if not self.current_description:
            print("No description available, skipping")
            return
        img_download_filepath = (
            Path.home() / "Desktop" / f"{self.current_name} Artwork.png"
        )
        revised_prompt, generated_img_url = self._mm._openai_agent.generate_image(
            f"Generate artwork based on the description I will provide below while adhering to the following constraints: 1. The artwork must utilize the art style of the 2024 Dungeons & Dragons Monster Manual (fantasy realism). 2. The artwork must depict the entire body of the creature, without any part of it cropped out of the frame. 3. The artwork must have a plain white background. 4. The artwork must not have any text on it whatsoever. The description to use as inspiration for the art is as follows: {self.current_description}",
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

    @property
    def current_name(self) -> str | None:
        return self._view.lineedit_name.text() or None

    @property
    def current_description(self) -> str | None:
        return self._view.textedit_description.toPlainText() or None

    @property
    def current_creature_type(self) -> MonsterType | None:
        mt = self._view.cb_creature_type.currentText()
        if mt:
            return MonsterType.from_display_name(mt)
        return None

    @property
    def current_alignment(self) -> Alignment | None:
        a = self._view.cb_alignment.currentText()
        if a:
            return Alignment.from_display_name(a)
        return None

    @property
    def current_size(self) -> Size | None:
        s = self._view.cb_size.currentText()
        if s:
            return Size.from_display_name(s)
        return None

    @property
    def current_challenge_rating(self) -> ChallengeRating | None:
        cr = self._view.lineedit_challenge_rating.text()
        if cr:
            return ChallengeRating(float(cr))
        return None

    @property
    def current_encounter_size(self) -> EncounterSize | None:
        es = self._view.cb_encounter_size.currentText()
        if es:
            return EncounterSize.from_display_name(es)
        return None

    @property
    def current_encounter_difficulty(self) -> EncounterDifficulty | None:
        ed = self._view.cb_encounter_difficulty.currentText()
        if ed:
            return EncounterDifficulty.from_display_name(ed)
        return None

    @property
    def current_avg_party_level(self) -> int | None:
        return self._view.spinbox_avg_party_lvl.value()

    @property
    def current_num_pcs(self) -> int | None:
        return self._view.spinbox_num_pcs.value()

    @property
    def current_skill_proficiencies(self) -> Sequence[tuple[Skill, Proficiency]]:
        pattern = re.compile(r"^(.*)\s\((.*)\)$")
        capture_group_skill_display_name = 1
        capture_group_proficiency_display_name = 2
        retval = []
        for i in range(self._view.listview_skills.count()):
            item_text = self._view.listview_skills.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            match = re.match(pattern, item_text)
            if match is None:
                raise RuntimeError
            skill_txt = match.group(capture_group_skill_display_name)
            skill = Skill.from_display_name(skill_txt)
            proficiency_txt = match.group(capture_group_proficiency_display_name)
            proficiency = Proficiency.from_display_name(proficiency_txt)
            retval.append((skill, proficiency))
        return retval

    @property
    def current_condition_immunities(self) -> Sequence[tuple[Condition, Resistance]]:
        pattern = re.compile(r"^(.*)\s\((.*)\)$")
        capture_group_condition_display_name = 1
        capture_group_resistance_display_name = 2
        retval = []
        for i in range(self._view.listview_conditions.count()):
            item_text = self._view.listview_conditions.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            match = re.match(pattern, item_text)
            if match is None:
                raise RuntimeError
            condition_txt = match.group(capture_group_condition_display_name)
            condition = Condition.from_display_name(condition_txt)
            resistance_txt = match.group(capture_group_resistance_display_name)
            resistance = Resistance.from_display_name(resistance_txt)
            retval.append((condition, resistance))
        return retval

    @property
    def current_damage_resistances(self) -> Sequence[tuple[DamageType, Resistance]]:
        pattern = re.compile(r"^(.*)\s\((.*)\)$")
        capture_group_dmg_display_name = 1
        capture_group_resistance_display_name = 2
        retval = []
        for i in range(self._view.listview_damage.count()):
            item_text = self._view.listview_damage.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            match = re.match(pattern, item_text)
            if match is None:
                raise RuntimeError
            dmg_txt = match.group(capture_group_dmg_display_name)
            dmg = DamageType.from_display_name(dmg_txt)
            resistance_txt = match.group(capture_group_resistance_display_name)
            resistance = Resistance.from_display_name(resistance_txt)
            retval.append((dmg, resistance))
        return retval

    @property
    def current_languages(self) -> Sequence[tuple[Language, LanguageProficiency]]:
        pattern = re.compile(r"^(.*)\s\((.*)\)$")
        capture_group_language_display_name = 1
        capture_group_language_proficiency_display_name = 2
        retval = []
        for i in range(self._view.listview_languages.count()):
            item_text = self._view.listview_languages.item(i).data(
                Qt.ItemDataRole.DisplayRole
            )
            match = re.match(pattern, item_text)
            if match is None:
                raise RuntimeError
            language_text = match.group(capture_group_language_display_name)
            language = Language.from_display_name(language_text)
            language_proficiency_text = match.group(
                capture_group_language_proficiency_display_name
            )
            language_proficiency = LanguageProficiency.from_display_name(
                language_proficiency_text
            )
            retval.append((language, language_proficiency))
        return retval

    @property
    def has_telepathy(self) -> bool:
        return self._view.checkbox_telepathy.checkState() == Qt.CheckState.Checked

    @property
    def telepathy_range_ft(self) -> int | None:
        if not self.has_telepathy:
            return None
        try:
            return int(self._view.lineedit_telepathy_range.text())
        except Exception as e:
            return None

    @property
    def tags(self) -> str:
        return ""  # TODO: Implement me

    @property
    def current_ac(self) -> int:
        return 10  # TODO: Implement me

    @property
    def current_hp(self) -> str:
        return "100 (5d20 + 0)"  # TODO: Implement me

    @property
    def current_speed(self) -> str:
        return "30 ft."  # TODO: Implement me

    @property
    def current_ability_scores(self) -> AbilityScores:
        return AbilityScores(
            {
                Ability.STRENGTH: self.strength,
                Ability.DEXTERITY: self.dex,
                Ability.CONSTITUTION: self.con,
                Ability.INTELLIGENCE: self.intelligence,
                Ability.WISDOM: self.wis,
                Ability.CHARISMA: self.cha,
            }
        )

    @property
    def current_initiative(self) -> str:
        return (
            f"+{self.dex_mod} ({self.dex})"
            if self.dex >= 10
            else f"-{self.dex_mod} ({self.dex})"
        )

    @property
    def skills_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def resistances_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def senses_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def languages_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def traits_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def actions_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def strength(self) -> int:
        return self._view.spinbox_str.value()

    @property
    def strength_mod(self) -> int:
        return self.current_ability_scores.strength_modifier

    @property
    def strength_save(self) -> int:
        return self.strength_mod  # TODO: Implement me

    @property
    def dex(self) -> int:
        return self._view.spinbox_dex.value()

    @property
    def dex_mod(self) -> int:
        return self.current_ability_scores.dexterity_modifier

    @property
    def dex_save(self) -> int:
        return self.dex_mod  # TODO: Implement me

    @property
    def con(self) -> int:
        return self._view.spinbox_con.value()

    @property
    def con_mod(self) -> int:
        return self.current_ability_scores.constitution_modifier

    @property
    def con_save(self) -> int:
        return self.con_mod  # TODO: Implement me

    @property
    def intelligence(self) -> int:
        return self._view.spinbox_int.value()

    @property
    def intelligence_mod(self) -> int:
        return self.current_ability_scores.intelligence_modifier

    @property
    def intelligence_save(self) -> int:
        return self.intelligence_mod  # TODO: Implement me

    @property
    def wis(self) -> int:
        return self._view.spinbox_wis.value()

    @property
    def wis_mod(self) -> int:
        return self.current_ability_scores.wisdom_modifier

    @property
    def wis_save(self) -> int:
        return self.wis_mod  # TODO: Implement me

    @property
    def cha(self) -> int:
        return self._view.spinbox_cha.value()

    @property
    def cha_mod(self) -> int:
        return self.current_ability_scores.charisma_modifier

    @property
    def cha_save(self) -> int:
        return self.cha_mod  # TODO: Implement me

    def _generate_homebrewery_v3_markdown(self, wide: bool = False) -> str:
        return (
            f"{{monster,frame{',wide' if wide else ''}\n"
            f"## {self.current_name}\n"
            f"*{self.current_size.display_name} {self.current_creature_type.display_name}{self.tags}, {self.current_alignment.display_name}*\n"
            "\n"
            "{{stats\n"
            "\n"
            "{{vitals\n"
            f"**AC** :: {self.current_challenge_rating.armor_class}\n"
            f"**HP** :: {self.current_challenge_rating.hit_points(self.current_ability_scores, self.current_size)}\n"
            f"**Speed** :: {self.current_speed}\n"
            "\column\n"
            f"**Initiative** :: {self.current_initiative}\n"
            "}}\n"
            "\n"
            "{{tables\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Str| {self.strength} | {self.strength_mod} | {self.strength_save} |\n"
            f"|Int| {self.intelligence} | {self.intelligence_mod} | {self.intelligence_save} |\n"
            "\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Dex| {self.dex} | {self.dex_mod} | {self.dex_save} |\n"
            f"|Wis| {self.wis} | {self.wis_mod} | {self.wis_save} |\n"
            "\n"
            "|   |   | MOD  | SAVE |\n"
            "|:--|:-:|:----:|:----:|\n"
            f"|Con| {self.con} | {self.con_mod} | {self.con_save} |\n"
            f"|Cha| {self.cha} | {self.cha_mod} | {self.cha_save} |\n"
            "}}\n"
            "\n"
            f"**Skills** :: {self.skills_display}\n"
            f"**Resistances** :: {self.resistances_display}\n"
            f"**Senses** :: {self.senses_display}\n"
            f"**Languages** :: {self.languages_display}\n"
            f"**CR** :: {self.current_challenge_rating.display}\n"
            "}}\n"
            "\n"
            "### Traits\n"
            f"{self.traits_display}\n"  # TODO: Implement me
            "### Actions\n"
            f"{self.actions_display}\n"  # TODO: Implement me
            "\n"
            "}}\n"
        )
