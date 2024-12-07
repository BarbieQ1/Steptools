import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QWidget, QFileDialog, QRubberBand
from PyQt5.QtCore import Qt, QRect, QSize
from mss import mss
from PIL import Image
from pyzbar.pyzbar import decode
import pytesseract
from datetime import datetime


class SnippingTool(QWidget):
    def __init__(self, monitor_geometry, callback):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.3)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        self.setGeometry(monitor_geometry)
        self.start_point = None
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_point, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.rubber_band.setGeometry(QRect(self.start_point, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            end_point = event.pos()
            snip_rect = QRect(self.start_point, end_point).normalized()
            self.rubber_band.hide()
            self.close()
            self.callback(snip_rect, self.geometry())


class MultiMonitorSnippingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("OCR/QR Tool")
        self.setGeometry(100, 100, 600, 800)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        self.monitor_layout = QWidget(self)
        self.monitor_layout.setGeometry(50, 50, 500, 300)
        self.monitor_layout.setStyleSheet("background-color: #1C1C1C;")
        self.output_box = QTextEdit(self)
        self.output_box.setGeometry(50, 370, 500, 300)
        self.output_box.setStyleSheet("background-color: #1C1C1C; color: white; font-size: 12px;")
        self.output_box.setReadOnly(True)
        clear_button = QPushButton("Clear Output", self)
        clear_button.setGeometry(50, 680, 100, 30)
        clear_button.setStyleSheet("background-color: #555555; color: white; font-size: 12px;")
        clear_button.clicked.connect(self.output_box.clear)
        export_button = QPushButton("Export", self)
        export_button.setGeometry(450, 680, 100, 30)
        export_button.setStyleSheet("background-color: #555555; color: white; font-size: 12px;")
        export_button.clicked.connect(self.export_output)
        self.setup_monitor_buttons()

    def setup_monitor_buttons(self):
        screens = QApplication.screens()
        min_x = min(screen.geometry().x() for screen in screens)
        min_y = min(screen.geometry().y() for screen in screens)
        max_x = max(screen.geometry().x() + screen.geometry().width() for screen in screens)
        max_y = max(screen.geometry().y() + screen.geometry().height() for screen in screens)
        total_width = max_x - min_x
        total_height = max_y - min_y
        layout_width = self.monitor_layout.width()
        layout_height = self.monitor_layout.height()
        offset_x = (layout_width - (total_width / total_width) * layout_width) // 2
        offset_y = (layout_height - (total_height / total_height) * layout_height) // 2
        for idx, screen in enumerate(screens):
            geom = screen.geometry()
            button_width = int((geom.width() / total_width) * layout_width)
            button_height = int((geom.height() / total_height) * layout_height)
            button_x = int(((geom.x() - min_x) / total_width) * layout_width + offset_x)
            button_y = int(((geom.y() - min_y) / total_height) * layout_height + offset_y)
            button = QPushButton(f"Monitor {idx + 1}", self.monitor_layout)
            button.setStyleSheet("background-color: #555555; color: white; font-size: 12px;")
            button.setGeometry(button_x, button_y, max(button_width, 50), max(button_height, 25))
            button.clicked.connect(lambda _, i=idx: self.start_snip(i))

    def start_snip(self, monitor_index):
        screen = QApplication.screens()[monitor_index]
        geometry = screen.geometry()
        self.snipping_tool = SnippingTool(geometry, self.capture_snip)
        self.snipping_tool.show()

    def capture_snip(self, snip_rect, monitor_geometry):
        left = monitor_geometry.left() + snip_rect.left()
        top = monitor_geometry.top() + snip_rect.top()
        width = snip_rect.width()
        height = snip_rect.height()
        with mss() as sct:
            monitor = {"left": left, "top": top, "width": width, "height": height}
            screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        self.process_image(img)

    def process_image(self, image):
        now = datetime.now()
        self.output_box.append(f"<span style='color: yellow;'>----- {now.strftime('%d.%m.%y %H:%M:%S')} -----</span>")

        # OCR
        text = pytesseract.image_to_string(image).strip()
        ocr_found = False
        if text:
            self.output_box.append(f"<span style='color: lightblue;'>OCR Text:</span>\n{text}\n")
            ocr_found = True

        # Barcode detection
        codes = decode(image)
        barcode_found = False
        if codes:
            for code in codes:
                self.output_box.append(f"<span style='color: lightgreen;'>Barcode:</span> {code.type}, {code.data.decode('utf-8')}\n")
                barcode_found = True
        
        if not ocr_found and not barcode_found:
            self.output_box.append("<span style='color: orange;'>No results detected.</span>\n")

    def export_output(self):
        now = datetime.now()
        file_name = now.strftime("%d.%m.%y_%H:%M") + ".txt"
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Output", file_name, "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_box.toPlainText())


def main():
    app = QApplication(sys.argv)
    main_window = MultiMonitorSnippingApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
