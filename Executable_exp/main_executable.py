# from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog
# from PySide6.QtGui import QPixmap
# from PySide6.QtCore import Qt
# from Filtering_function import apply_filter
# import sys

import sys
import os
import PySide6
os.environ["QT_PLUGIN_PATH"] = os.path.join(os.path.dirname(PySide6.__file__), "plugins")

from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from Filtering_function import apply_filter

class ImageProcessorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processor")
        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()
        self.label = QLabel("Drag and drop an image here or click to select.", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 16px;")
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        self.setAcceptDrops(True)
        self.resize(600, 600)  # Ventana cuadrada al iniciar
        
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
        
    def process_image(self, file_path):
        print(f"Processing image: {file_path}")
        try:
            result = apply_filter(file_path, max_area=256*256)
            self.display_output(result)
        except Exception as e:
            print(f"Error processing image: {e}")
        
    def display_output(self, result):
        processed_image = result.processed_image.convert("RGB")
                
        # Convert processed_image to QImage
        qimage = QImage(processed_image.tobytes(), processed_image.width, processed_image.height, QImage.Format_RGB888)
        
        # Now use QPixmap.fromImage with the correct argument type
        pixmap = QPixmap.fromImage(qimage)
        
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    window = ImageProcessorApp()
    window.show()
    app.exec()