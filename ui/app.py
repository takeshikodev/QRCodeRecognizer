import os
import cv2
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit,
    QFrame, QSplitter, QApplication, QStatusBar, 
    QAction, QToolBar, QMenu, QMessageBox,
    QScrollArea, QSizePolicy, QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QResizeEvent
from PyQt5.QtCore import Qt, QSize, QTimer, QEvent
from detectors.qr_detector import QRCodeDetector
from ui.styles import (
    MAIN_WINDOW_STYLE, BUTTON_STYLE, IMAGE_FRAME_STYLE,
    TITLE_STYLE, RESULT_TITLE_STYLE, FRAME_STYLE,
    CARD_STYLE, STATUS_BAR_STYLE, SUCCESS_BUTTON_STYLE
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qr_detector = QRCodeDetector()
        self.original_image = None
        self.processed_image = None
        self.init_ui()
        
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._display_current_image)
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("QR Code Recognizer")
        self.setFixedSize(1280, 720)
        
        self.center_window()
        
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(STATUS_BAR_STYLE)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready to work")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet(FRAME_STYLE)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        self.splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QFrame()
        left_panel.setObjectName("card")
        left_panel.setStyleSheet(CARD_STYLE)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_frame = QLabel("DRAG IMAGE HERE\nOR CLICK 'SELECT IMAGE' BUTTON")
        self.image_frame.setObjectName("imageLabel")
        self.image_frame.setAlignment(Qt.AlignCenter)
        self.image_frame.setMinimumSize(700, 500)
        self.image_frame.setStyleSheet(IMAGE_FRAME_STYLE)
        self.image_frame.setWordWrap(True)
        self.image_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_frame.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        image_layout.addWidget(self.image_frame)
        scroll_area.setWidget(image_container)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.select_button = QPushButton("Select Image")
        self.select_button.setIcon(self.style().standardIcon(QApplication.style().SP_DialogOpenButton))
        self.select_button.setStyleSheet(BUTTON_STYLE)
        self.select_button.clicked.connect(self.load_image)
        
        self.save_button = QPushButton("Save Result")
        self.save_button.setStyleSheet(SUCCESS_BUTTON_STYLE)
        self.save_button.setIcon(self.style().standardIcon(QApplication.style().SP_DialogSaveButton))
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setEnabled(False)  # Disabled until QR codes are detected
        
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.save_button)
        
        left_layout.addWidget(scroll_area)
        left_layout.addLayout(button_layout)
        
        right_panel = QFrame()
        right_panel.setObjectName("card")
        right_panel.setStyleSheet(CARD_STYLE)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        result_title = QLabel("Scan Results")
        result_title.setObjectName("resultTitleLabel")
        result_title.setStyleSheet(RESULT_TITLE_STYLE)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        
        right_layout.addWidget(result_title)
        right_layout.addWidget(self.result_text)
        
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([int(self.width() * 0.7), int(self.width() * 0.3)])
        
        content_layout.addWidget(self.splitter)
        main_layout.addWidget(content_frame, 1)
        
        self.setAcceptDrops(True)
    
    def center_window(self):
        """Center window on screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize event"""
        super().resizeEvent(event)
        self.resize_timer.start(150)
    
    def _display_current_image(self):
        """Update display of current image"""
        if self.processed_image is not None:
            self._display_image(self.processed_image)
        
    def dragEnterEvent(self, event):
        """Handle drag enter event for file dropping"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        """Handle file drop event in application window"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files and self._is_valid_image_file(files[0]):
            self.process_image_file(files[0])
    
    def _is_valid_image_file(self, file_path):
        """Check if image format is valid"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        return os.path.splitext(file_path.lower())[1] in valid_extensions
        
    def load_image(self):
        """Load image through file dialog"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_name:
            self.statusBar.showMessage(f"Loading image: {os.path.basename(file_name)}")
            QApplication.processEvents()
            self.process_image_file(file_name)
    
    def process_image_file(self, file_path):
        """Process selected image file"""
        self.original_image = cv2.imread(file_path)
        if self.original_image is None:
            self.result_text.setText("Error loading image")
            self.statusBar.showMessage("Error loading image")
            return
        
        self.statusBar.showMessage("Processing image...")
        self.process_image()
    
    def process_image(self):
        """Process image and detect QR codes"""
        if self.original_image is None:
            return
            
        results, self.processed_image = self.qr_detector.detect_qr_codes(self.original_image)
        
        self._display_image(self.processed_image)
        
        if results:
            self.save_button.setEnabled(True)
            result_text = "QR codes found:\n\n"
            for i, data in enumerate(results, 1):
                try:
                    decoded_data = data.data.decode('utf-8', errors='replace')
                    result_text += f"{i}. Type: {data.type}\nData: {decoded_data}\n\n"
                except Exception as e:
                    result_text += f"{i}. Type: {data.type}\nDecoding error: {str(e)}\n\n"
            
            self.statusBar.showMessage(f"QR codes found: {len(results)}")
        else:
            self.save_button.setEnabled(False)
            result_text = "No QR codes found"
            self.statusBar.showMessage("No QR codes found")
        
        self.result_text.setText(result_text)
    
    def _display_image(self, image):
        """Display image in the interface with proper scaling"""
        if image is None:
            return
        
        frame_width = self.image_frame.width() - 20
        frame_height = self.image_frame.height() - 20
        
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        if width > height:
            new_width = min(width, frame_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, frame_height)
            new_width = int(new_height * aspect_ratio)
        
        if new_width > frame_width:
            new_width = frame_width
            new_height = int(new_width / aspect_ratio)
        
        if new_height > frame_height:
            new_height = frame_height
            new_width = int(new_height * aspect_ratio)
        
        scaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        bytes_per_line = 3 * new_width
        qt_image = QImage(
            cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB).data,
            new_width, new_height, bytes_per_line, QImage.Format_RGB888
        )
        
        self.image_frame.setPixmap(QPixmap.fromImage(qt_image))
    
    def save_result(self):
        """Save the recognition result to file"""
        if self.processed_image is None:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Result",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        
        if file_name:
            try:
                cv2.imwrite(file_name, self.processed_image)
                self.result_text.append("\nResult saved to file: " + file_name)
                self.statusBar.showMessage(f"Result saved: {os.path.basename(file_name)}")
                
                QMessageBox.information(
                    self, 
                    "Save Complete", 
                    f"Image successfully saved to file:\n{file_name}"
                )
            except Exception as e:
                self.statusBar.showMessage(f"Save error: {str(e)}")
                QMessageBox.critical(
                    self,
                    "Save Error",
                    f"Failed to save image: {str(e)}"
                )