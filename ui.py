from aqt.qt import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar, QPushButton, QPixmap
from .badge_manager import get_all_badge_data, calculate_total_xp, get_current_rank, get_next_rank_info
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QMovie, QFont, QFontDatabase, QPixmap, QPalette, QBrush
from PyQt6 import QtCore
import os

#set font
font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PixelifySans-Medium.ttf")
font_id = QFontDatabase.addApplicationFont(font_path)
font_families = QFontDatabase.applicationFontFamilies(font_id)

def get_badge_icon_path(tier_name):
    base_path = os.path.join(os.path.dirname(__file__), "assets", "badges")
    
    if tier_name is None or tier_name == 0:
        return os.path.join(base_path, "badge_locked.png")  # Replace with your locked icon if needed
    
    tier_label = tier_name.lower()
    filename = f"badge_{tier_label}.png"
    return os.path.join(base_path, filename)

def show_main_window():
    dialog = QDialog()
    dialog_width = 750
    dialog_height = 670
    dialog.setFixedWidth(dialog_width)
    dialog.setFixedHeight(dialog_height)

    overlay = QLabel(dialog)
    overlay.resize(dialog.size())
    overlay.setStyleSheet("background-color: rgba(0, 0, 0, 40);")
    overlay.lower()

    bg_path = os.path.join(os.path.dirname(__file__), "assets", "background", "hospital2.png")
    pixmap = QPixmap(bg_path)
    if not pixmap.isNull():
        scaled_pixmap = pixmap.scaled(dialog.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(dialog.backgroundRole(), QBrush(scaled_pixmap))
        dialog.setPalette(palette)
        dialog.setAutoFillBackground(True)
    else:
        print("Failed to load background image:", bg_path)

    dialog.setWindowTitle("Quest of the White Coat")

    layout = QVBoxLayout()

    badge_data = get_all_badge_data()
    total_xp = calculate_total_xp(badge_data)
    rank = get_current_rank(total_xp)
    next_rank, next_threshold = get_next_rank_info(total_xp)

    welcome_label = QLabel("Welcome to Quest of the White Coat!")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    welcome_font = QFont(font_families[0], 32, QFont.Weight.Bold)
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

    rank_label = QLabel(f"Rank: {rank} ({total_xp} XP)")
    rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    rank_font = QFont(font_families[0], 25)
    rank_label.setFont(rank_font)
    rank_label.setStyleSheet("color: #FFFFFF;")
    layout.addWidget(rank_label)

    # rank progress bar
    if next_rank:
        progress_bar = QProgressBar()
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 5px;
                background-color: #222;
            }
            QProgressBar::chunk {
                background-color: #00bfa5;
                width: 10px;
                margin: 0.5px;
            }
        """)
        progress_bar.setTextVisible(False)
        #xp_to_next = next_threshold - total_xp
        progress = int((total_xp / next_threshold) * 100)
        progress_bar.setValue(progress)
        layout.addWidget(progress_bar)

        progress_label = QLabel(f"{progress}% to {next_rank}")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_font = QFont(font_families[0], 16)
        progress_label.setFont(progress_font)
        layout.addWidget(progress_label)
    else:
        layout.addWidget(QLabel("🏆 Max Rank Achieved!"))


    open_badges_btn = QPushButton("View Badge Collection")
    open_badges_btn.setStyleSheet("""
        QPushButton {
            background-color: #00bfa5;
            color: white;
            border-radius: 5px;
            padding: 6px 12px;
            width: 65%;
            font-weigh: bold;
            f"font-family: '{font_family}';"
        }
        QPushButton:hover {
            background-color: #00a893;
            border: 2px solid #ffffff;
        }
    """)
    button_font = QFont(font_families[0])
    open_badges_btn.setFont(button_font)
    open_badges_btn.clicked.connect(show_badge_popup)

    btn_width = int(dialog_width * 0.65)
    open_badges_btn.setFixedWidth(btn_width)

    btn_container = QHBoxLayout()
    btn_container.addStretch()
    btn_container.addWidget(open_badges_btn)
    btn_container.addStretch()

    layout.addLayout(btn_container)

    #layout.addWidget(open_badges_btn)

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
        name_font = QFont(font_families[0], 14)
        name_label.setFont(name_font)

        badge_layout.addWidget(icon_label)
        badge_layout.addWidget(name_label)

        progress = QProgressBar()
        progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 5px;
                background-color: #222;
            }
            QProgressBar::chunk {
                background-color: #00bfa5;
                width: 10px;
                margin: 0.5px;
            }
        """)
        progress.setTextVisible(False)
        progress.setValue(int(data["progress"] * 100))
        badge_layout.addWidget(progress)

        grid.addLayout(badge_layout, row, col)
        col += 1
        if col >= 3:
            col = 0
            row += 1
    
    layout.addLayout(grid)

    close_badges_btn = QPushButton("⬅ Back to Home")
    close_badges_btn.setStyleSheet("""
        QPushButton {
            background-color: #00bfa5;
            color: white;
            border-radius: 5px;
            padding: 6px 12px;
            width: 65%;
            font-weigh: bold;
            f"font-family: '{font_family}';"
        }
        QPushButton:hover {
            background-color: #00a893;
            border: 2px solid #ffffff;
        }
    """)
    button_font = QFont(font_families[0])
    close_badges_btn.setFont(button_font)
    close_badges_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_badges_btn)

    dialog.setLayout(layout)
    dialog.exec()