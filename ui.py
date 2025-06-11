from aqt.qt import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar, QPushButton
from .badge_manager import get_all_badge_data


def show_main_window():
    dialog = QDialog()
    dialog.setWindowTitle("Quest of the White Coat")

    layout = QVBoxLayout()
    layout.addWidget(QLabel("🩺 Welcome to the Quest!"))

    open_badges_btn = QPushButton("View Badge Collection")
    open_badges_btn.clicked.connect(show_badge_popup)
    layout.addWidget(open_badges_btn)

    dialog.setLayout(layout)
    dialog.exec()


def show_badge_popup():
    badge_data = get_all_badge_data()

    dialog = QDialog()
    dialog.setWindowTitle("Your Badges")

    layout = QVBoxLayout()

    grid = QGridLayout()
    row = col = 0

    for subject, data in badge_data.items():
        badge_layout = QVBoxLayout()

        if data["tier"] is None:
            icon_label = QLabel("❓")
            name_label = QLabel("???")
        else:
            icon_label = QLabel(f"🏅 {data['tier']}")
            name_label = QLabel(subject)

        icon_label.setAlignment(Qt.AlignCenter)
        name_label.setAlignment(Qt.AlignCenter)

        badge_layout.addWidget(icon_label)
        badge_layout.addWidget(name_label)

        progress = QProgressBar()
        progress.setValue(int(data["progress"] * 100))
        badge_layout.addWidget(progress)

        # Wrap in a container widget
        container = QVBoxLayout()
        for widget in badge_layout.children():
            if isinstance(widget, QLabel) or isinstance(widget, QProgressBar):
                container.addWidget(widget)

        grid.addLayout(badge_layout, row, col)
        col += 1
        if col >= 3:
            col = 0
            row += 1

    layout.addLayout(grid)
    dialog.setLayout(layout)
    dialog.exec()