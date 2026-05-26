from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTranslateAi")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.title_label = QLabel("SmartTranslateAi")
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text here...")
        self.translate_button = QPushButton("Translate")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.output_text)
