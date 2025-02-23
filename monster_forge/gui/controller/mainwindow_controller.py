from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5.QtCore import Qt
from monster_forge.gui.controller.monster_creation_controller import (
    MonsterCreationController,
)
from monster_forge.gui.view.monster_maker_mainwindow_view import Ui_MainWindow


class MainWindowController(QMainWindow):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self._app = app
        self._view = Ui_MainWindow()
        self._view.setupUi(self)
        self.setWindowTitle("Monster Maker")
        self._view.btn_create_monster.clicked.connect(self._create_new_monster)
        self._creation_subcontroller: MonsterCreationController | None = None

    def _create_new_monster(self) -> None:
        self._creation_subcontroller = MonsterCreationController()
        self._creation_subcontroller.setWindowModality(
            Qt.WindowModality.ApplicationModal
        )
        self._creation_subcontroller.show()

    def run(self) -> None:
        self.show()
        sys.exit(self._app.exec_())
