from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.fallback_generator import FallbackGenerator
from app.ollama_client import OllamaClient
from app.parser import RequestParser
from app.prompt_builder import PromptBuilder


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.parser = RequestParser()
        self.prompt_builder = PromptBuilder()
        self.fallback = FallbackGenerator()
        self.setWindowTitle("ESP32 MicroPython Generator + Ollama")
        self.resize(1300, 820)
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        title = QLabel("Generator MicroPython koda za ESP32 iz hrvatskog teksta")
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)

        self.model_edit = QLineEdit("qwen2.5-coder:7b")
        self.output_edit = QLineEdit(str(Path("generated") / "main.py"))
        self.use_fallback = QCheckBox("Ako Ollama padne, koristi lokalni fallback generator")
        self.use_fallback.setChecked(True)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Primjer: Učitaj temperaturu i vlagu sa dht22 svake dve sekunde i blicni 200 ms led na esp32 GPIO02"
        )

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setLineWrapMode(QTextEdit.NoWrap)
        code_font = QFont("Consolas")
        code_font.setPointSize(10)
        self.output_text.setFont(code_font)

        self.status_label = QLabel("Spremno.")

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Ollama model:"))
        top_row.addWidget(self.model_edit)
        top_row.addWidget(QLabel("Spremi u:"))
        top_row.addWidget(self.output_edit)

        button_row = QHBoxLayout()
        btn_generate = QPushButton("Generiraj i spremi .py")
        btn_generate.clicked.connect(self.generate_and_save)
        btn_example = QPushButton("Primjer")
        btn_example.clicked.connect(self.load_example)
        btn_clear = QPushButton("Očisti")
        btn_clear.clicked.connect(self.clear_all)
        button_row.addWidget(btn_generate)
        button_row.addWidget(btn_example)
        button_row.addWidget(btn_clear)
        button_row.addStretch()

        editors = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()
        left.addWidget(QLabel("Ulaz"))
        left.addWidget(self.input_text)
        right.addWidget(QLabel("Generirani kod"))
        right.addWidget(self.output_text)
        editors.addLayout(left, 1)
        editors.addLayout(right, 1)

        root.addWidget(title)
        root.addLayout(top_row)
        root.addWidget(self.use_fallback)
        root.addLayout(editors)
        root.addLayout(button_row)
        root.addWidget(self.status_label)

    def load_example(self) -> None:
        self.input_text.setPlainText(
            "Učitaj temperaturu i vlagu sa dht22 svake dve sekunde i blicni 200 ms led na esp32 GPIO02"
        )

    def clear_all(self) -> None:
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("Očišćeno.")

    def generate_and_save(self) -> None:
        user_text = self.input_text.toPlainText().strip()
        if not user_text:
            QMessageBox.warning(self, "Upozorenje", "Upiši tekstualni zahtjev.")
            return

        parsed = self.parser.parse(user_text)
        prompt = self.prompt_builder.build(parsed)
        client = OllamaClient(model=self.model_edit.text().strip() or "qwen2.5-coder:7b")
        save_path = Path(self.output_edit.text().strip() or "generated/main.py")

        try:
            code = client.generate_code(prompt)
            source = "Ollama"
        except Exception as exc:
            if not self.use_fallback.isChecked():
                QMessageBox.critical(self, "Greška", str(exc))
                self.status_label.setText(f"Greška: {exc}")
                return
            code = self.fallback.generate(parsed)
            source = "fallback"
            self.status_label.setText(f"Ollama nije uspjela, korišten je fallback. Razlog: {exc}")

        self.output_text.setPlainText(code)

        try:
            saved_to = client.save_code(code, save_path)
        except Exception as exc:
            QMessageBox.critical(self, "Greška", f"Kod je generiran, ali nije spremljen: {exc}")
            return

        self.status_label.setText(f"Kod generiran iz izvora: {source}. Spremljeno u: {saved_to}")


def run_app() -> None:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
