from __future__ import annotations
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSignal
from monster_forge.gui.view.trait_view import Ui_TraitView
from monster_forge.dnd.action import CombatCharacteristic


class CombatCharacteristicController(QWidget):
    deleted = pyqtSignal()

    def __init__(
        self, cc: CombatCharacteristic, *, parent: QObject | None = None
    ) -> None:
        super().__init__(parent=parent)
        self.cc = cc
        self._view = Ui_TraitView()
        self._view.setupUi(self)
        self._view.btn_delete_trait.clicked.connect(self.deleted.emit)
        self._view.lbl_trait.setText(self.cc.homebrewery_v3_2024_markdown)

    @staticmethod
    def generate(
        monster_name: str, monster_description: str
    ) -> CombatCharacteristicController:
        pass
