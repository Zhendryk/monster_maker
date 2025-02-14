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
)


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_MonsterCreationView()
        self._view.setupUi(self)
        self._mm = MonsterMaker()
        self._connect_signals_to_slots()

    def _connect_signals_to_slots(self) -> None:
        self._view.btn_refine_description.clicked.connect(self._refine_monster_concept)
        self._view.btn_generate_names.clicked.connect(self._suggest_monster_names)
        self._view.cb_skills.addItems([s.display_name for s in Skill])
        self._view.cb_skills.setCurrentIndex(-1)
        self._view.cb_alignment.addItems(
            [alignment.display_name for alignment in Alignment]
        )
        self._view.cb_alignment.setCurrentIndex(-1)
        self._view.cb_encounter_difficulty.addItems(
            [diff.display_name for diff in EncounterDifficulty]
        )
        self._view.cb_encounter_difficulty.setCurrentIndex(-1)
        self._view.cb_encounter_size.addItems(
            [size.display_name for size in EncounterSize]
        )
        self._view.cb_encounter_size.setCurrentIndex(-1)
        self._view.cb_conditions.addItems(
            [condition.display_name for condition in Condition]
        )
        self._view.cb_conditions.setCurrentIndex(-1)
        self._view.cb_creature_type.addItems([mt.display_name for mt in MonsterType])
        self._view.cb_creature_type.setCurrentIndex(-1)
        self._view.cb_languages.addItems([l.display_name for l in Language])
        self._view.cb_languages.setCurrentIndex(-1)
        self._view.cb_size.addItems([s.display_name for s in Size])
        self._view.cb_size.setCurrentIndex(-1)

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
    def current_monster_concept(self) -> str:
        return self._view.textedit_description.toPlainText()
