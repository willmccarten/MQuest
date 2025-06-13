from aqt.qt import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar, QPushButton
from .badge_manager import get_all_badge_data, calculate_total_xp, get_current_rank, get_next_rank_info
from PyQt6.QtCore import Qt

def show_main_window():
    dialog = QDialog()
    dialog.setWindowTitle("Quest of the White Coat")

    layout = QVBoxLayout()

    badge_data = get_all_badge_data()
    total_xp = calculate_total_xp(badge_data)
    rank = get_current_rank(total_xp)
    next_rank, next_threshold = get_next_rank_info(total_xp)

    welcome_label = QLabel("🩺 Welcome to the Quest!")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    rank_label = QLabel(f"👩‍⚕️ Rank: {rank} ({total_xp} XP)")
    rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(welcome_label)
    layout.addWidget(rank_label)

    # rank progress bar
    if next_rank:
        progress_bar = QProgressBar()
        xp_to_next = next_threshold - total_xp
        progress = int((total_xp / next_threshold) * 100)
        progress_bar.setValue(progress)
        layout.addWidget(progress_bar)

        progress_label = QLabel(f"{progress}% to {next_rank} ({total_xp}/{next_threshold} XP)")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(progress_label)
    else:
        layout.addWidget(QLabel("🏆 Max Rank Achieved!"))


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

        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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