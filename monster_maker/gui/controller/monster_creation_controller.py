from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from monster_maker.gui.view.monster_creation_view import (
    Ui_MonsterCreationView,
)


class MonsterCreationController(QWidget):
    def __init__(self, *, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._view = Ui_MonsterCreationView()
        self._view.setupUi(self)
