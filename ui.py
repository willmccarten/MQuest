from aqt.qt import QDialog, QLabel, QVBoxLayout
from .badge_manager import get_all_badge_data

def show_main_window():
    dialog = QDialog()
    dialog.setWindowTitle("Quest of the White Coat")

    layout = QVBoxLayout()

    badge_data = get_all_badge_data()
    for subject, data in badge_data.items():
        line = f"{subject}: {data['tier']} ({int(data['progress'] * 100)}%)"
        layout.addWidget(QLabel(line))

    dialog.setLayout(layout)
    dialog.exec()
