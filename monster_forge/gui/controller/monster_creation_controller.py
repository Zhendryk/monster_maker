from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from ..view.monster_creation_view import (
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
)


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_MonsterCreationView()
        self._view.setupUi(self)
        self._mm = MonsterMaker()
        self._setup_UI()

    def _setup_UI(self) -> None:
        self._view.progressbar_main.setVisible(False)
        self._view.progressbar_generate_all.setVisible(False)
        self._view.btn_refine_description.clicked.connect(self._refine_monster_concept)
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

    def _refine_monster_concept(self) -> None:
        print("Refining monster concept...")
        if not self.current_monster_concept:
            raise RuntimeError
        refined_concept = self._mm.refine_monster_concept(self.current_monster_concept)
        print(f"Refined: {refined_concept}")

    def _suggest_monster_names(self) -> None:
        print("Suggesting names...")
        suggested_names = self._mm.suggest_names(self.current_monster_concept)
        self._view.lineedit_name.setText(", ".join(suggested_names))

    @property
    def current_name(self) -> str | None:
        return self._view.lineedit_name.text() or None

    @property
    def current_description(self) -> str | None:
        return self._view.textedit_description.toPlainText() or None

    @property
    def current_creature_type(self) -> MonsterType | None:
        mt = self._view.cb_creature_type.currentText()
        if mt is not None:
            return MonsterType.from_display_name(mt)
        return None

    @property
    def current_alignment(self) -> Alignment | None:
        a = self._view.cb_alignment.currentText()
        if a is not None:
            return Alignment.from_display_name(a)
        return None

    @property
    def current_size(self) -> Size | None:
        s = self._view.cb_size.currentText()
        if s is not None:
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
