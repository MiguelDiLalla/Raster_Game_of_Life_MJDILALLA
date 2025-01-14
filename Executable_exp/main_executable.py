import sys
import os
import PySide6
os.environ["QT_PLUGIN_PATH"] = os.path.join(os.path.dirname(PySide6.__file__), "plugins")

from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QPushButton
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from Filtering_function import apply_filter
import numpy as np

class ImageProcessorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processor")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window borders
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Make background fully transparent
        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()

        # Add image label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: white; font-size: 16px;")

        # Add text label
        self.text_label = QLabel("Drop", self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("color: white; font-size: 14px; background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 10px;")
        self.text_label.setFixedSize(200, 50)

        # Add 'X' button to close the application
        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("color: white; font-size: 14px; background-color: red; border: none;")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)

        # Add components to layout
        self.layout.addWidget(self.close_button, alignment=Qt.AlignBottom | Qt.AlignRight)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.text_label, alignment=Qt.AlignBottom | Qt.AlignLeft)
        self.setLayout(self.layout)

        self.setAcceptDrops(True)

        self.current_result = None  # To store the result of the last processed image

        # Set default black square
        self.set_default_image()

    def set_default_image(self):
        # pass a  randomly generated image of balck and white pixels

        # Create a black square image using numpy
        image_array = np.zeros((256, 256, 3), dtype=np.uint8)  # Black square
        height, width, channels = image_array.shape
        qimage = QImage(
            image_array.data, width, height, channels * width, QImage.Format_RGB888
        )
        # Create a random array of ones and zeros
        image_array = np.random.randint(0, 2, (256, 256, 3), dtype=np.uint8) * 255  # Random black and white pixels
        height, width, channels = image_array.shape
        qimage = QImage(
            image_array.data, width, height, channels * width, QImage.Format_RGB888
        )

        # process the image
        # Save QImage to a temporary file
        temp_file_path = "temp_image.png"
        qimage.save(temp_file_path)

        # Process the image using the temporary file path
        self.current_result = apply_filter(temp_file_path, max_area=256*256)

        # Remove the temporary file after processing
        os.remove(temp_file_path)
        processed_image = self.current_result.processed_image.convert("RGB")
        image_array = np.array(processed_image)
        height, width, channels = image_array.shape
        qimage = QImage(
            image_array.data, width, height, channels * width, QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(False)

        # Resize window to match the default black square
        self.setFixedSize(width, height)

        # Show text label
        self.text_label.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.process_image(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_path:
                self.process_image(file_path)
        elif event.button() == Qt.RightButton:
            self.save_image() ##respect this change

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()

    def process_image(self, file_path):
        print(f"Processing image: {file_path}")
        try:
            self.current_result = apply_filter(file_path, max_area=256*256)
            self.display_output(self.current_result)
        except Exception as e:
            print(f"Error processing image: {e}")

    def display_output(self, result):
        processed_image = result.processed_image.convert("RGB")
        image_array = np.array(processed_image)  # Convert to numpy array
        height, width, channels = image_array.shape
        qimage = QImage(
            image_array.data, width, height, channels * width, QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(False)

        # Resize window to match the image size without borders
        self.setFixedSize(width, height)

        # Hide text label after displaying an image
        self.text_label.hide()

    def save_image(self):
        if self.current_result:
            suggested_name = f"{self.current_result.metadata.get('hash', 'processed_image')}.png"
            print(f"Saving processed image as: {suggested_name}")
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Processed Image",
                suggested_name,
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if file_path:
                self.current_result.save(file_path)


if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    window = ImageProcessorApp()
    window.show()
    app.exec()
