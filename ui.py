from aqt.qt import QDialog, QLabel, QVBoxLayout

def show_main_window():
    dialog = QDialog()
    dialog.setWindowTitle("Quest of the White Coat")
    
    layout = QVBoxLayout()
    label = QLabel("🩺 Welcome to the Quest!\nMore coming soon...")
    layout.addWidget(label)

    dialog.setLayout(layout)
    dialog.exec()
