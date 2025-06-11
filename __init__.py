from aqt import mw
from aqt.qt import QAction, QDialog, QLabel, QVBoxLayout
from aqt.utils import showInfo
import anki
import aqt

# Import our UI (we'll build this out later)
from .ui import show_main_window

# Add menu item to open the add-on manually
action = QAction("Quest of the White Coat", mw)
action.triggered.connect(show_main_window)
mw.form.menuTools.addAction(action)
