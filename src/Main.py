"""
Main Application File
"""
import sys

from PyQt6.QtWidgets import QApplication

from models.GameModel import GameModel
from widgets.GameWidget import GameWidget
from utils.ExceptionUtils import except_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_model = GameModel()
    game_widget = GameWidget(game_model)
    game_widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
