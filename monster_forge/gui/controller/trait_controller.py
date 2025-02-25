from __future__ import annotations
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from monster_forge.gui.view.trait_view import Ui_TraitView
from monster_forge.dnd.trait import Trait


class TraitController(QWidget):
    deleted = pyqtSignal()

    def __init__(self, trait: Trait, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self.trait = trait
        self._view = Ui_TraitView()
        self._view.setupUi(self)
        self._view.btn_delete_trait.clicked.connect(self.deleted.emit)
        self._view.lbl_trait.setText(self.trait.display_str())

    @staticmethod
    def generate(monster_name: str, monster_description: str) -> TraitController:
        pass
