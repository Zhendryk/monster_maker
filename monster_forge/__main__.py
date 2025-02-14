import sys
from PyQt5.QtWidgets import QApplication
from monster_forge.gui.controller.mainwindow_controller import MainWindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindowController(app)
    main_window.run()
