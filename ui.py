from aqt.qt import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar, QPushButton, QPixmap
from .badge_manager import get_all_badge_data, calculate_total_xp, get_current_rank, get_next_rank_info
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie, QFont
from PyQt6 import QtCore
import os

def get_badge_icon_path(tier_name):
    base_path = os.path.join(os.path.dirname(__file__), "assets", "badges")
    
    if tier_name is None or tier_name == 0:
        return os.path.join(base_path, "badge_locked.png")  # Replace with your locked icon if needed
    
    tier_label = tier_name.lower()
    filename = f"badge_{tier_label}.png"
    return os.path.join(base_path, filename)

def show_main_window():
    dialog = QDialog()
    dialog.setWindowTitle("Quest of the White Coat")

    layout = QVBoxLayout()

    badge_data = get_all_badge_data()
    total_xp = calculate_total_xp(badge_data)
    rank = get_current_rank(total_xp)
    next_rank, next_threshold = get_next_rank_info(total_xp)

    welcome_label = QLabel("Welcome to the Quest of the White Coat!")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    welcome_font = QFont("Courier New", 32, QFont.Weight.Bold)
    welcome_label.setFont(welcome_font)
    welcome_label.setStyleSheet("color: #FFFFFF;")
    layout.addWidget(welcome_label)

    sprite_label = QLabel()
    movie = QMovie(os.path.join(os.path.dirname(__file__), "assets", "character", "character_sprite.gif"))
    movie.setScaledSize(QtCore.QSize(420, 420))  # Adjust size here (try 120x120 or bigger)
    sprite_label.setMovie(movie)
    sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    movie.start()
    layout.addWidget(sprite_label)

    rank_label = QLabel(f"🩺 Rank: {rank} ({total_xp} XP)")
    rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    rank_font = QFont("Courier New", 25, QFont.Weight.Bold)
    rank_label.setFont(rank_font)
    rank_label.setStyleSheet("color: #FFFFFF;")
    layout.addWidget(rank_label)

    # rank progress bar
    if next_rank:
        progress_bar = QProgressBar()
        xp_to_next = next_threshold - total_xp
        progress = int((total_xp / next_threshold) * 100)
        progress_bar.setValue(progress)
        layout.addWidget(progress_bar)

        progress_label = QLabel(f"{progress}% to {next_rank}")
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

        #load in badge icon art
        icon_label = QLabel()
        icon_path = get_badge_icon_path(data["tier"])
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if data["tier"] is None:
            name_label = QLabel("???")
        else:
            name_label = QLabel(subject)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        badge_layout.addWidget(icon_label)
        badge_layout.addWidget(name_label)

        progress = QProgressBar()
        progress.setValue(int(data["progress"] * 100))
        badge_layout.addWidget(progress)

        grid.addLayout(badge_layout, row, col)
        col += 1
        if col >= 3:
            col = 0
            row += 1

    layout.addLayout(grid)
    dialog.setLayout(layout)
    dialog.exec()