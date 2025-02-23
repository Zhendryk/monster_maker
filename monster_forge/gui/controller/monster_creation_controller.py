from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from collections.abc import Sequence
from PyQt5.QtCore import QObject, Qt
import re
from monster_forge.gui.view.create_monster_view import Ui_CreateMonsterView
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
    SpeedType,
)
from pathlib import Path
from functools import partial
from random import randint

# A demon who disguises itself amongst the cultural and financial elite, attending soirees and other lavish events. It lures in its victims with its impeccable charm and decorum.

# A demon who blends into the higher eschelons of society to hunt its prey. It regularly attends soirees and other elegant events to lure victims in with its charming personality and impeccable decorum.


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_CreateMonsterView()
        self._view.setupUi(self)
        self._mm = MonsterMaker()
        self._setup_UI()

    def _setup_UI(self) -> None:
        self.setWindowTitle("Create New Monster")
        self._view.progressbar_ai_query.setVisible(False)
        self._view.btn_refine_description.clicked.connect(self._refine_description)
        self._view.btn_suggest_name.clicked.connect(self._suggest_monster_names)
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
        language_items = []
        for l in Language:
            language_items.append(l.display_name)
            if l.plus_amt > 0:
                language_items.extend(
                    [l.display_name_plus_x(i) for i in range(l.plus_amt, 1)]
                )
        self._view.cb_languages.addItems(sorted(language_items))
        self._view.cb_languages.setCurrentIndex(-1)
        self._view.cb_size.addItems(sorted([s.display_name for s in Size]))
        self._view.cb_size.setCurrentIndex(-1)
        self._view.cb_size.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_damage.addItems(sorted([d.display_name for d in DamageType]))
        self._view.cb_damage.setCurrentIndex(-1)
        self._view.lineedit_challenge_rating.setEnabled(False)
        self._view.cb_encounter_size.currentIndexChanged.connect(self._calc_cr)
        self._view.cb_encounter_difficulty.currentIndexChanged.connect(self._calc_cr)
        self._view.spinbox_avg_party_level.valueChanged.connect(self._calc_cr)
        self._view.spinbox_num_pcs.valueChanged.connect(self._calc_cr)
        self._view.btn_generate_artwork.clicked.connect(self._generate_artwork)
        self._view.btn_suggest_creature_type.clicked.connect(
            self._suggest_creature_type
        )
        self._view.btn_suggest_alignment.clicked.connect(self._suggest_alignment)
        self._view.btn_suggest_size.clicked.connect(self._suggest_size)
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
        self._view.btn_languages_add.clicked.connect(
            partial(self._add_language, LanguageProficiency.UNDERSTANDS)
        )
        self._view.btn_languages_all.clicked.connect(self._add_all_languages)
        self._view.btn_languages_remove.clicked.connect(self._remove_language)
        self._view.btn_conditions_immune.clicked.connect(self._add_condition_immunity)
        self._view.btn_conditions_remove.clicked.connect(
            self._remove_condition_immunity
        )
        self._view.checkbox_tie_ac_to_cr.clicked.connect(self._toggle_ac_cr_tie)
        self._view.checkbox_tie_hp_to_cr.clicked.connect(self._toggle_hp_cr_tie)
        self._view.btn_suggest_ability_scores.clicked.connect(
            self._suggest_ability_scores
        )
        self._view.btn_suggest_all.clicked.connect(self._generate_all)
        self._view.btn_generate_markdown.clicked.connect(self.generate_markdown_file)
        self._view.checkbox_telepathy.clicked.connect(self._telepathy_toggled)

    def _telepathy_toggled(self, enabled: bool) -> None:
        self._view.spinbox_telepathy_range.setEnabled(enabled)

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
            self._view._lbl_per_monster_for_x_monsters.setText(
                f"per monster, for {encounter.num_monsters} monsters"
            )
            if (
                self.current_challenge_rating is not None
                and self._view.checkbox_tie_ac_to_cr.isChecked()
            ):
                self._view.spinbox_ac.setValue(
                    self.current_challenge_rating.armor_class
                )
            if (
                self.current_challenge_rating is not None
                and self._view.checkbox_tie_hp_to_cr.isChecked()
            ):
                if self.current_size is not None:
                    self._view.lineedit_hp.setText(
                        self.current_challenge_rating.hit_points(
                            self.current_ability_scores, self.current_size
                        )
                    )

    def _generate_all(self) -> None:
        if not self.current_description:
            print("Can't generate monster without a description. Aborting...")
            return
        if not self.current_name:
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
        if not self.current_description:
            raise RuntimeError  # TODO: Generate description
        refined_concept = self._mm.refine_monster_concept(self.current_description)
        print(f"Refined: {refined_concept}")
        self._view.textedit_description.setText(refined_concept)

    def _suggest_monster_names(self) -> None:
        print("Suggesting names...")
        suggested_names = self._mm.suggest_names(self.current_description)
        name = suggested_names[randint(0, len(suggested_names) - 1)].strip(", ")
        self._view.lineedit_name.setText(name)

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
            f"Given the provided D&D 5E 2024 monster name and description, suggest an appropriate size for it. Your response must be one of the following sizes and nothing else: {', '.join([s.display_name for s in Size])}. The name of the monster is: {self.current_name}. The description of the monster is: {self.current_description}"
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
        if not self.current_name:
            print("Monster name required to generate ability scores.")
            return
        if not self.current_description:
            print("Monster description required to generate ability scores.")
            return
        if not self.current_challenge_rating:
            print("Monster challenge rating required to generate ability scores")
            return
        suggested_scores_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name, description and challenge rating, suggest a set of ability scores for it. Your response must include key-value pairs of the form SCORE_NAME:SCORE_VALUE where SCORE_NAME is Strength,Dexterity,Constitution,Intelligence,Wisdom or Charisma, and SCORE_VALUE is any number 0-30. You must generate one key-value pair for each SCORE_NAME, and no other text whatsoever. The monster's name is: {self.current_name}. The Monster's Challenge Rating is: {self.current_challenge_rating.rating}. The Monster's description is: {self.current_description}."
        )
        suggested_score_lines = [
            sl.replace(" ", "") for sl in suggested_scores_txt.split("\n")
        ]
        suggested_scores = {
            Ability.from_display_name(sl.split(":")[0]): int(sl.split(":")[1])
            for sl in suggested_score_lines
        }
        ab_sc = AbilityScores(suggested_scores)
        self._view.spinbox_str.setValue(ab_sc.scores[Ability.STRENGTH])
        self._view.spinbox_dex.setValue(ab_sc.scores[Ability.DEXTERITY])
        self._view.spinbox_con.setValue(ab_sc.scores[Ability.CONSTITUTION])
        self._view.spinbox_int.setValue(ab_sc.scores[Ability.INTELLIGENCE])
        self._view.spinbox_wis.setValue(ab_sc.scores[Ability.WISDOM])
        self._view.spinbox_cha.setValue(ab_sc.scores[Ability.CHARISMA])

    def text_prompt(
        self, givens: dict[str, str], suggestions: list[str], must_includes: list[str]
    ) -> str:
        s = f"Given the provided D&D 5E monster {', '.join(givens.keys())}, suggest {', '.join(suggestions)} for it. Your response must include {', '.join(must_includes)}, and no other text whatsoever."
        for given_title, given_value in givens.items():
            s = s + f" The monster's {given_title} is: {given_value}."
        return s

    def _suggest_encounter(self) -> None:
        if not self.current_name:
            print("Monster name required to generate ability scores.")
            return
        if not self.current_description:
            print("Monster description required to generate ability scores.")
            return
        print("Suggesting encounter statistics...")
        suggested_encounter_txt = self._mm._openai_agent.generate_text(
            f"Given the provided D&D 5E 2024 monster name and description, suggest appropriate encounter statistics for it. Your response must include key-value pairs of the form KEY:VALUE where KEY is Size,Difficulty,Number of Player Characters and Average Party Level. For the Key 'Size', the valid values are SINGLETON, SMALL, MEDIUM LARGE, SWARM. For the key 'Difficulty', the valid values are LOW, MODERATE and HIGH. For the key 'Number of Player Characters', the valid values are an integer 1-8. For the key 'Average Party Level', the valid values are an integer 1-20. You must generate 1 key-value pair for each KEY, and no other text whatsoever. The monster's name is: {self.current_name}. The monster's description is: {self.current_description}"
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

    def _add_language(self, proficiency_level: LanguageProficiency) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
        if any(
            (
                self._view.listwidget_languages.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(language.display_name)
                for i in range(self._view.listwidget_languages.count())
            )
        ):
            print(
                f'"{language.display_name} ({proficiency_level.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listwidget_languages.addItem(
            f"{language.display_name} ({proficiency_level.display_name})"
        )

    def _add_all_languages(self) -> None:
        pass

    def _remove_language(self) -> None:
        lang_text = self._view.cb_languages.currentText()
        language = Language.from_display_name(lang_text)
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

    def _add_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
        if any(
            (
                self._view.listwidget_conditions.item(i)
                .data(Qt.ItemDataRole.DisplayRole)
                .startswith(condition.display_name)
                for i in range(self._view.listwidget_conditions.count())
            )
        ):
            print(
                f'"{condition.display_name} ({Resistance.IMMUNE.display_name})" already exists, not adding duplicate...'
            )
            return
        self._view.listwidget_conditions.addItem(
            f"{condition.display_name} ({Resistance.IMMUNE.display_name})"
        )

    def _remove_condition_immunity(self) -> None:
        condition_text = self._view.cb_conditions.currentText()
        condition = Condition.from_display_name(condition_text)
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
        return self._view.spinbox_avg_party_level.value()

    @property
    def current_num_pcs(self) -> int | None:
        return self._view.spinbox_num_pcs.value()

    @property
    def current_skill_proficiencies(self) -> Sequence[tuple[Skill, Proficiency]]:
        pattern = re.compile(r"^(.*)\s\((.*)\)$")
        capture_group_skill_display_name = 1
        capture_group_proficiency_display_name = 2
        retval = []
        for i in range(self._view.listwidget_skills.count()):
            item_text = self._view.listwidget_skills.item(i).data(
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
        for i in range(self._view.listwidget_conditions.count()):
            item_text = self._view.listwidget_conditions.item(i).data(
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
        for i in range(self._view.listwidget_damage.count()):
            item_text = self._view.listwidget_damage.item(i).data(
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
        for i in range(self._view.listwidget_languages.count()):
            item_text = self._view.listwidget_languages.item(i).data(
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
        return self._view.spinbox_ac.value()

    @property
    def current_hp(self) -> str:
        return self._view.lineedit_hp.text()

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
    def current_speed(self) -> dict[SpeedType, int]:
        return {
            SpeedType.WALKING: self._view.spinbox_walk_speed.value(),
            SpeedType.SWIM: self._view.spinbox_swim_speed.value(),
            SpeedType.CLIMB: self._view.spinbox_climb_speed.value(),
            SpeedType.BURROW: self._view.spinbox_burrow_speed.value(),
            SpeedType.FLY: self._view.spinbox_fly_speed.value(),
        }

    @property
    def speed_display(self) -> str:
        cs = self.current_speed
        st = ""
        walk_speed = f"{cs[SpeedType.WALKING]} ft."
        additional_speeds = []
        alphabetical_types = sorted(
            [s for s in SpeedType if s != SpeedType.WALKING],
            key=lambda x: x.name.lower(),
        )
        for speed_type in alphabetical_types:
            if cs[speed_type] != 0:
                additional_speeds.append(
                    f"{speed_type.name.capitalize()} {cs[speed_type]} ft."
                )
        if additional_speeds:
            additional_speeds.insert(0, walk_speed)
            st = ", ".join(additional_speeds)
        else:
            st = walk_speed
        return st

    @property
    def current_initiative(self) -> str:
        return (
            f"+{self.dex_mod} ({self.dex})"
            if self.dex >= 10
            else f"-{self.dex_mod} ({self.dex})"
        )

    @property
    def skills_display(self) -> str:
        if self.current_challenge_rating is None:
            return ""
        retval = []
        ab_sc = self.current_ability_scores
        for skill, proficiency in sorted(
            self.current_skill_proficiencies, key=lambda x: x[0].display_name
        ):
            skill_mod = ab_sc._calculate_modifier(
                ab_sc.scores[skill.associated_ability]
            )
            pb = self.current_challenge_rating.proficiency_bonus
            match proficiency:
                case Proficiency.NORMAL:
                    total_bonus = skill_mod
                case Proficiency.PROFICIENT:
                    total_bonus = skill_mod + pb
                case Proficiency.EXPERTISE:
                    total_bonus = skill_mod + (2 * pb)
                case _:
                    raise NotImplementedError
            retval.append(f"{skill.display_name} +{total_bonus}")
        return ", ".join(retval)

    @property
    def resistances_display(self) -> str:
        dmg_resistances = sorted(
            [
                dr[0].display_name
                for dr in self.current_damage_resistances
                if dr[1] == Resistance.RESISTANT
            ],
            key=lambda x: x[0].display_name,
        )
        return ", ".join(dmg_resistances)

    @property
    def immunities_display(self) -> str:
        dmg_immunities = sorted(
            [
                dr[0].display_name
                for dr in self.current_damage_resistances
                if dr[1] == Resistance.IMMUNE
            ],
            key=lambda x: x[0].display_name,
        )
        condition_immunities = sorted(
            [ci[0].display_name for ci in self.current_condition_immunities],
            key=lambda x: x[0].display_name,
        )
        return ", ".join(dmg_immunities) + "; " + ", ".join(condition_immunities)

    @property
    def senses_display(self) -> str:
        return ""  # TODO: Implement me

    @property
    def languages_display(self) -> str:
        # TODO: Add "All" and "Common plus x other languages" options
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
        if self._view.checkbox_prof_st_str.isChecked():
            return self.strength_mod + self.current_challenge_rating.proficiency_bonus
        return self.strength_mod

    @property
    def dex(self) -> int:
        return self._view.spinbox_dex.value()

    @property
    def dex_mod(self) -> int:
        return self.current_ability_scores.dexterity_modifier

    @property
    def dex_save(self) -> int:
        if self._view.checkbox_prof_st_dex.isChecked():
            return self.dex_mod + self.current_challenge_rating.proficiency_bonus
        return self.dex_mod

    @property
    def con(self) -> int:
        return self._view.spinbox_con.value()

    @property
    def con_mod(self) -> int:
        return self.current_ability_scores.constitution_modifier

    @property
    def con_save(self) -> int:
        if self._view.checkbox_prof_st_con.isChecked():
            return self.con_mod + self.current_challenge_rating.proficiency_bonus
        return self.con_mod

    @property
    def intelligence(self) -> int:
        return self._view.spinbox_int.value()

    @property
    def intelligence_mod(self) -> int:
        return self.current_ability_scores.intelligence_modifier

    @property
    def intelligence_save(self) -> int:
        if self._view.checkbox_prof_st_int.isChecked():
            return (
                self.intelligence_mod + self.current_challenge_rating.proficiency_bonus
            )
        return self.intelligence_mod

    @property
    def wis(self) -> int:
        return self._view.spinbox_wis.value()

    @property
    def wis_mod(self) -> int:
        return self.current_ability_scores.wisdom_modifier

    @property
    def wis_save(self) -> int:
        if self._view.checkbox_prof_st_wis.isChecked():
            return self.wis_mod + self.current_challenge_rating.proficiency_bonus
        return self.wis_mod

    @property
    def cha(self) -> int:
        return self._view.spinbox_cha.value()

    @property
    def cha_mod(self) -> int:
        return self.current_ability_scores.charisma_modifier

    @property
    def cha_save(self) -> int:
        if self._view.checkbox_prof_st_cha.isChecked():
            return self.cha_mod + self.current_challenge_rating.proficiency_bonus
        return self.cha_mod

    def _generate_homebrewery_v3_markdown(self, wide: bool = False) -> str:
        return (
            f"{{{{monster,frame{',wide' if wide else ''}\n"
            f"## {self.current_name}\n"
            f"*{self.current_size.display_name} {self.current_creature_type.display_name}{self.tags}, {self.current_alignment.display_name}*\n"
            "\n"
            "{{stats\n"
            "\n"
            "{{vitals\n"
            f"**AC** :: {self.current_ac}\n"
            f"**HP** :: {self.current_hp}\n"
            f"**Speed** :: {self.speed_display}\n"
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

    def generate_markdown_file(
        self,
        checked: bool,
        output_path: Path | None = None,
        wide_statblock: bool = False,
    ) -> None:
        if output_path is None:
            fn = self.current_name.lower().replace(" ", "_")
            output_path = Path(f"C:\\Users\\Jon\\Desktop\\{fn}_statblock.md")
        with open(output_path, "w") as markdown_file:
            markdown_txt = self._generate_homebrewery_v3_markdown(wide=wide_statblock)
            markdown_file.write(markdown_txt)
        print(f"File write complete: {output_path}")
