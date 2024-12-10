import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from image_iterator import ImageIterator

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """
        Инициализирует главное окно приложения и элементы интерфейса.
        """
        super().__init__()
        self.setWindowTitle("Image Viewer")

        self.image_iterator = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel("Select file annotations", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.select_annotation_button = QPushButton("Select annotation file", self)
        self.select_annotation_button.clicked.connect(self.select_annotation_file)
        self.layout.addWidget(self.select_annotation_button)

        self.next_image_button = QPushButton("Next image", self)
        self.next_image_button.clicked.connect(self.show_next_image)
        self.next_image_button.setEnabled(False)
        self.layout.addWidget(self.next_image_button)

    def select_annotation_file(self) -> None:
        """
        Открывает диалоговое окно для выбора файла аннотации и создает итератор изображений.

        :return: None
        """
        annotation_file, _ = QFileDialog.getOpenFileName(self, "Select Annotation File", filter="CSV Files (*.csv)")
        if annotation_file:
            self.image_iterator = ImageIterator(annotation_file)
            self.next_image_button.setEnabled(True)
            self.show_next_image()

    def show_next_image(self) -> None:
        """
        Отображает следующее изображение из итератора на метке.
        Если изображения закончились, кнопка становится неактивной.

        :return: None
        """
        if self.image_iterator:
            try:
                absolute_path = next(self.image_iterator)
                if os.path.exists(absolute_path):
                    pixmap = QPixmap(absolute_path)
                    self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
                else:
                    self.image_label.setText(f"File not found: {absolute_path}")
            except StopIteration:
                self.image_label.setText("End of dataset")
                self.next_image_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
