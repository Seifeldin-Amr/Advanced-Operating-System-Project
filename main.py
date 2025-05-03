import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QScrollArea, 
                            QFrame, QLineEdit, QRadioButton, QButtonGroup,
                            QTextEdit, QMessageBox, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter, QPen
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qt_material import apply_stylesheet
import numpy as np
from virtual_memory import FIFO, SecondChance
from disk_scheduling import SCAN, LOOK

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Algorithms Simulator")
        self.setMinimumSize(1200, 800)
        
        # Set background gradient
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                stop:0 #f5f7fa, stop:1 #e4e8ef);
            }
        """)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Create stacked widget to hold all pages
        self.stacked_widget = QStackedWidget()
        
        # Create home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(30)
        
        # Header container with shadow effect
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(15)
        
        # Title with icon
        title_layout = QHBoxLayout()
        icon_label = QLabel()

        # Create a custom computer icon
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.transparent)  # Start with transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw monitor
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1565C0"))  # Blue color matching title
        painter.drawRoundedRect(4, 4, 40, 26, 2, 2)  # Monitor body

        # Draw screen
        painter.setBrush(QColor("#e0f7fa"))  # Light blue screen
        painter.drawRect(8, 8, 32, 18)  # Screen area

        # Draw CPU/tower
        painter.setBrush(QColor("#1565C0"))  # Blue color matching title
        painter.drawRoundedRect(16, 30, 16, 14, 2, 2)  # Tower base

        # Draw keyboard
        painter.setBrush(QColor("#78909c"))  # Gray color for keyboard
        painter.drawRoundedRect(10, 44, 28, 3, 1, 1)  # Keyboard

        # Draw details on tower
        painter.setPen(QPen(QColor("#e0f7fa"), 1))
        painter.drawLine(20, 34, 28, 34)  # Power button
        painter.drawLine(20, 38, 28, 38)  # Disk drive

        # Add circuit pattern on screen
        painter.setPen(QPen(QColor("#0d47a1"), 1))
        painter.drawLine(14, 17, 22, 17)  # Horizontal line
        painter.drawLine(34, 13, 34, 21)  # Vertical line
        painter.drawLine(26, 13, 26, 21)  # Vertical line
        painter.drawLine(26, 13, 34, 13)  # Horizontal line
        painter.drawLine(26, 21, 34, 21)  # Horizontal line

        painter.end()
        icon_label.setPixmap(pixmap)
        title_layout.addWidget(icon_label)
        
        title = QLabel("OS Algorithms Simulator")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #1565C0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title, 1)
        header_layout.addLayout(title_layout)
        
        # Description
        desc = QLabel("Select the type of algorithm you want to simulate:")
        desc.setFont(QFont("Segoe UI", 14))
        desc.setStyleSheet("color: #455A64;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(desc)
        
        home_layout.addWidget(header_container)
        
        # Buttons container
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(30, 30, 30, 30)
        buttons_layout.setSpacing(40)
        
        # Virtual Memory button with icon and shadow
        vm_button = QPushButton()
        vm_button.setMinimumSize(300, 200)
        vm_layout = QVBoxLayout(vm_button)
        vm_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vm_layout.setSpacing(15)
        
        vm_icon = QLabel()
        # Create a colored square with a memory icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)  # Start with transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw memory chip representation
        painter.setPen(Qt.PenStyle.SolidLine)
        painter.setBrush(QColor("#2196F3"))  # Blue color for the chip
        painter.setBrush(QColor("white"))
        # Main chip body
        painter.drawRect(8, 12, 48, 40)
        # Pins on chip
        for i in range(6):
            painter.drawRect(10 + i*8, 6, 4, 6)  # Top pins
            painter.drawRect(10 + i*8, 52, 4, 6)  # Bottom pins
        painter.end()
        vm_icon.setPixmap(pixmap)
        vm_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vm_layout.addWidget(vm_icon)
        
        vm_text = QLabel("Virtual Memory\nAlgorithms")
        vm_text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        vm_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vm_layout.addWidget(vm_text)
        
        vm_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                padding: 20px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #1976D2;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLabel {
                color: white;
            }
        """)
        vm_button.clicked.connect(self.show_virtual_memory)
        buttons_layout.addWidget(vm_button)
        
        # Disk Scheduling button with icon and shadow
        ds_button = QPushButton()
        ds_button.setMinimumSize(300, 200)
        ds_layout = QVBoxLayout(ds_button)
        ds_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ds_layout.setSpacing(15)
        
        ds_icon = QLabel()
        # Create a custom hard drive icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)  # Start with transparent background
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw hard drive body
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("white"))
        painter.drawRoundedRect(4, 8, 56, 48, 4, 4)  # Main hard drive body

        # Add drive details
        painter.setPen(QPen(QColor("#333333"), 1))
        # Activity light
        painter.setBrush(QColor("#4CAF50"))  # Green LED
        painter.drawRect(48, 16, 6, 4)  # Activity LED

        # Disk platters
        painter.setBrush(QColor("#e0e0e0"))  # Light gray for platters
        painter.drawEllipse(12, 16, 32, 32)  # Outer disk
        painter.setBrush(QColor("#cccccc"))  # Darker gray for inner platter
        painter.drawEllipse(20, 24, 16, 16)  # Inner disk
        painter.setBrush(QColor("#999999"))  # Even darker for center
        painter.drawEllipse(26, 30, 4, 4)  # Center spindle

        # Add magnetic arm
        painter.setPen(QPen(QColor("#333333"), 2))  # Thicker pen for the arm
        painter.drawLine(28, 32, 48, 40)  # Draw the arm from center to edge
        # Draw the arm head
        painter.setBrush(QColor("#666666"))
        painter.drawRect(46, 38, 6, 5)  # Magnetic head at end of arm

        # Add connector lines at bottom
        painter.setPen(QPen(QColor("#333333"), 1))  # Reset to normal pen

        painter.end()
        ds_icon.setPixmap(pixmap)
        ds_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ds_layout.addWidget(ds_icon)
        
        ds_text = QLabel("Disk Scheduling\nAlgorithms")
        ds_text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        ds_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ds_layout.addWidget(ds_text)
        
        ds_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 15px;
                padding: 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #388E3C;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #1B5E20;
            }
            QLabel {
                color: white;
            }
        """)
        ds_button.clicked.connect(self.show_disk_scheduling)
        buttons_layout.addWidget(ds_button)
        
        home_layout.addWidget(buttons_container)
        home_layout.addStretch()
        
        # Create the Virtual Memory page
        self.vm_page = self.create_virtual_memory_page()
        
        # Create the Disk Scheduling page
        self.ds_page = self.create_disk_scheduling_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(home_page)
        self.stacked_widget.addWidget(self.vm_page)
        self.stacked_widget.addWidget(self.ds_page)
        
        main_layout.addWidget(self.stacked_widget)

    def show_virtual_memory(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_disk_scheduling(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_home(self):
        self.stacked_widget.setCurrentIndex(0)

    def create_virtual_memory_page(self):
        vm_page = QWidget()
        layout = QVBoxLayout(vm_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Add back button at the top
        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Segoe UI", 11))  # Correct size for a button
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #455A64;
                color: white;
                border-radius: 8px;
                padding: 10px 16px;
                text-align: left;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #37474F;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #263238;
            }
        """)

        # Create a custom back arrow icon
        arrow_icon = QPixmap(20, 20)
        arrow_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(arrow_icon)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("white"), 2))
        # Draw arrow
        painter.drawLine(15, 10, 5, 10)  # Horizontal line
        painter.drawLine(5, 10, 10, 5)   # Upper diagonal
        painter.drawLine(5, 10, 10, 15)  # Lower diagonal
        painter.end()

        # Set the custom icon
        back_button.setIcon(QIcon(arrow_icon))
        back_button.setIconSize(QSize(20, 20))

        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        back_button.clicked.connect(self.show_home)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Title
        title = QLabel("Virtual Memory Algorithms")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        # Algorithm selection
        algo_group = QButtonGroup()
        algo_frame = QFrame()
        algo_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        algo_layout = QVBoxLayout(algo_frame)
        
        algo_label = QLabel("Select Algorithm:")
        algo_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        algo_layout.addWidget(algo_label)
        
        self.fifo_radio = QRadioButton("FIFO")
        self.fifo_radio.setFont(QFont("Segoe UI", 11))
        self.fifo_radio.setChecked(True)
        algo_group.addButton(self.fifo_radio)
        algo_layout.addWidget(self.fifo_radio)
        
        self.second_chance_radio = QRadioButton("Second Chance")
        self.second_chance_radio.setFont(QFont("Segoe UI", 11))
        algo_group.addButton(self.second_chance_radio)
        algo_layout.addWidget(self.second_chance_radio)
        
        content_layout.addWidget(algo_frame)
        
        # Input fields
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        input_label = QLabel("Input Parameters:")
        input_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        input_layout.addWidget(input_label)
        
        # Frames input
        frames_layout = QHBoxLayout()
        frames_label = QLabel("Number of Frames:")
        frames_label.setFont(QFont("Segoe UI", 11))
        self.frames_input = QLineEdit()
        self.frames_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        frames_layout.addWidget(frames_label)
        frames_layout.addWidget(self.frames_input)
        input_layout.addLayout(frames_layout)
        
        # Reference string input
        ref_layout = QHBoxLayout()
        ref_label = QLabel("Reference String (comma-separated):")
        ref_label.setFont(QFont("Segoe UI", 11))
        self.ref_input = QLineEdit()
        self.ref_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        ref_layout.addWidget(ref_label)
        ref_layout.addWidget(self.ref_input)
        input_layout.addLayout(ref_layout)
        
        content_layout.addWidget(input_frame)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.vm_run_button = QPushButton("Run Simulation")
        self.vm_run_button.setFont(QFont("Segoe UI", 11))
        self.vm_run_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.vm_run_button.clicked.connect(self.run_vm_simulation)
        
        self.vm_reset_button = QPushButton("Reset")
        self.vm_reset_button.setFont(QFont("Segoe UI", 11))
        self.vm_reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.vm_reset_button.clicked.connect(self.reset_vm)
        
        buttons_layout.addWidget(self.vm_run_button)
        buttons_layout.addWidget(self.vm_reset_button)
        content_layout.addLayout(buttons_layout)
        
        # Results area
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #ddd;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setSpacing(20)  # Increased spacing

        results_label = QLabel("Results:")
        results_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))  # Increased font size
        results_layout.addWidget(results_label)

        self.vm_results_text = QTextEdit()
        self.vm_results_text.setReadOnly(True)
        self.vm_results_text.setMinimumHeight(180)  # Set minimum height
        self.vm_results_text.setFont(QFont("Consolas", 12))  # Use monospace font for better readability
        self.vm_results_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                color: #333333;
                line-height: 1.5;
            }
        """)
        results_layout.addWidget(self.vm_results_text)
        
        # Visualization area
        self.vm_visualization_widget = QWidget()
        self.vm_visualization_widget.setMinimumHeight(400)
        self.vm_visualization_widget.setLayout(QVBoxLayout())  # Initialize layout
        results_layout.addWidget(self.vm_visualization_widget)
        
        content_layout.addWidget(results_frame)
        
        # Set up scroll area
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return vm_page

    def create_disk_scheduling_page(self):
        ds_page = QWidget()
        layout = QVBoxLayout(ds_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Add back button at the top for disk scheduling page
        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Segoe UI", 11))  # Correct size for a button
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #455A64;
                color: white;
                border-radius: 8px;
                padding: 10px 16px;
                text-align: left;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #37474F;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #263238;
            }
        """)

        # Create a custom back arrow icon
        arrow_icon = QPixmap(20, 20)
        arrow_icon.fill(Qt.GlobalColor.transparent)
        painter = QPainter(arrow_icon)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("white"), 2))
        # Draw arrow
        painter.drawLine(15, 10, 5, 10)  # Horizontal line
        painter.drawLine(5, 10, 10, 5)   # Upper diagonal
        painter.drawLine(5, 10, 10, 15)  # Lower diagonal
        painter.end()

        # Set the custom icon
        back_button.setIcon(QIcon(arrow_icon))
        back_button.setIconSize(QSize(20, 20))

        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        back_button.clicked.connect(self.show_home)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Title
        title = QLabel("Disk Scheduling Algorithms")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        # Algorithm selection
        algo_group = QButtonGroup()
        algo_frame = QFrame()
        algo_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        algo_layout = QVBoxLayout(algo_frame)
        
        algo_label = QLabel("Select Algorithm:")
        algo_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        algo_layout.addWidget(algo_label)
        
        self.scan_radio = QRadioButton("SCAN")
        self.scan_radio.setFont(QFont("Segoe UI", 11))
        self.scan_radio.setChecked(True)
        algo_group.addButton(self.scan_radio)
        algo_layout.addWidget(self.scan_radio)
        
        self.look_radio = QRadioButton("LOOK")
        self.look_radio.setFont(QFont("Segoe UI", 11))
        algo_group.addButton(self.look_radio)
        algo_layout.addWidget(self.look_radio)
        
        content_layout.addWidget(algo_frame)
        
        # Input fields
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        input_label = QLabel("Input Parameters:")
        input_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        input_layout.addWidget(input_label)
        
        # Cylinders input
        cyl_layout = QHBoxLayout()
        cyl_label = QLabel("Number of Cylinders:")
        cyl_label.setFont(QFont("Segoe UI", 11))
        self.cylinders_input = QLineEdit()
        self.cylinders_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        cyl_layout.addWidget(cyl_label)
        cyl_layout.addWidget(self.cylinders_input)
        input_layout.addLayout(cyl_layout)
        
        # Current position input
        pos_layout = QHBoxLayout()
        pos_label = QLabel("Current Position:")
        pos_label.setFont(QFont("Segoe UI", 11))
        self.current_pos_input = QLineEdit()
        self.current_pos_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        pos_layout.addWidget(pos_label)
        pos_layout.addWidget(self.current_pos_input)
        input_layout.addLayout(pos_layout)
        
        # Queue input
        queue_layout = QHBoxLayout()
        queue_label = QLabel("Request Queue (comma-separated):")
        queue_label.setFont(QFont("Segoe UI", 11))
        self.queue_input = QLineEdit()
        self.queue_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        queue_layout.addWidget(queue_label)
        queue_layout.addWidget(self.queue_input)
        input_layout.addLayout(queue_layout)
        
        content_layout.addWidget(input_frame)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.ds_run_button = QPushButton("Run Simulation")
        self.ds_run_button.setFont(QFont("Segoe UI", 11))
        self.ds_run_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.ds_run_button.clicked.connect(self.run_ds_simulation)
        
        self.ds_reset_button = QPushButton("Reset")
        self.ds_reset_button.setFont(QFont("Segoe UI", 11))
        self.ds_reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.ds_reset_button.clicked.connect(self.reset_ds)
        
        buttons_layout.addWidget(self.ds_run_button)
        buttons_layout.addWidget(self.ds_reset_button)
        content_layout.addLayout(buttons_layout)
        
        # Results area
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #ddd;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setSpacing(20)  # Increased spacing

        results_label = QLabel("Results:")
        results_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))  # Increased font size
        results_layout.addWidget(results_label)

        self.ds_results_text = QTextEdit()
        self.ds_results_text.setReadOnly(True)
        self.ds_results_text.setMinimumHeight(180)  # Set minimum height
        self.ds_results_text.setFont(QFont("Consolas", 12))  # Use monospace font for better readability
        self.ds_results_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                color: #333333;
                line-height: 1.5;
            }
        """)
        results_layout.addWidget(self.ds_results_text)
        
        # Visualization area
        self.ds_visualization_widget = QWidget()
        self.ds_visualization_widget.setMinimumHeight(400)
        self.ds_visualization_widget.setLayout(QVBoxLayout())  # Initialize layout
        results_layout.addWidget(self.ds_visualization_widget)
        
        content_layout.addWidget(results_frame)
        
        # Set up scroll area
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return ds_page

    def run_vm_simulation(self):
        try:
            frames = int(self.frames_input.text())
            if frames <= 0:
                raise ValueError("Number of frames must be positive")
            
            ref_string = [int(x.strip()) for x in self.ref_input.text().split(',')]
            if not all(x >= 0 for x in ref_string):
                raise ValueError("Reference string values must be non-negative")
            
            algorithm = "FIFO" if self.fifo_radio.isChecked() else "SecondChance"
            
            if algorithm == "FIFO":
                results = FIFO(frames, ref_string)
            else:
                results = SecondChance(frames, ref_string)
            
            self.display_vm_results(results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))

    def display_vm_results(self, results):
        self.vm_results_text.clear()
        self.vm_results_text.append(f"Page Faults: {results['faults']}")
        self.vm_results_text.append(f"Page Hits: {results['hits']}")
        self.vm_results_text.append(f"Total References: {len(results['access_type'])}")
        self.vm_results_text.append(f"Hit Rate: {(results['hits'] / len(results['access_type']) * 100):.1f}%")
        self.vm_results_text.append(f"Fault Rate: {(results['faults'] / len(results['access_type']) * 100):.1f}%\n")
        self.vm_results_text.append("Allocation Sequence:")
        
        for step in results['sequence']:
            self.vm_results_text.append(str(step))
        
        self.visualize_vm_results(results)

    def visualize_vm_results(self, results):
        # Clear previous visualization
        for i in reversed(range(self.vm_visualization_widget.layout().count())): 
            self.vm_visualization_widget.layout().itemAt(i).widget().setParent(None)
        
        # Create new figure with two subplots
        fig = plt.figure(figsize=(16, 10))  # Increased figure size
        
        # Main grid subplot
        ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=4)  # Increased rowspan
        sequence = results['sequence']
        frames = len(sequence[0])
        steps = len(sequence)
        access_type = results['access_type']
        ref_string = results['ref_string']
        
        # Check if this is Second Chance algorithm
        is_second_chance = 'reference_bits' in results
        ref_bits = results.get('reference_bits', None)
        
        # Create a grid with more padding
        ax1.set_xlim(-1, steps)  # Added padding on both sides
        ax1.set_ylim(frames - 0.5, -2.2 if is_second_chance else -1.8)  # Extra space for ref bits
        
        # Remove axis lines and ticks but keep bottom border
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(True)  # Keep bottom border
        ax1.spines['left'].set_visible(False)
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Plot reference string and hit/fault indicators at the top
        for i in range(steps):
            # Status indicator
            color = '#117711' if access_type[i] else '#990000'
            indicator = 'H' if access_type[i] else 'F'
            ax1.text(i, -1.2, indicator, ha='center', va='center', 
                    fontsize=12, color=color, fontweight='bold')
            
            # Reference string - show the actual reference value
            ref_value = ref_string[i] if i < len(ref_string) else sequence[i][-1]
            ax1.text(i, -0.8, str(ref_value), ha='center', va='center',
                    fontsize=12, fontweight='bold')
        
        # Plot grid cells with pages
        for step in range(steps):
            for frame in range(frames):
                page = sequence[step][frame]
                if page is not None:
                    # Draw cell with brighter colors
                    color = '#AAFFAA' if access_type[step] else '#FFAAAA'  # Lighter pastel colors
                    rect = plt.Rectangle((step - 0.4, frame - 0.4), 0.8, 0.8, 
                                      fill=True, facecolor=color, 
                                      edgecolor='black', alpha=0.7)
                    ax1.add_patch(rect)
                    # Add page number
                    ax1.text(step, frame, str(page), ha='center', va='center', 
                           fontsize=12, fontweight='bold')
                    
                    # Add reference bit indicator for Second Chance
                    if is_second_chance and ref_bits and ref_bits[step][frame] == 1:
                        ax1.text(step + 0.3, frame - 0.3, "★", ha='center', va='center',
                                fontsize=8, color='#0000FF')
                
                # Draw cell borders
                rect = plt.Rectangle((step - 0.5, frame - 0.5), 1, 1, 
                                   fill=False, edgecolor='black', linewidth=0.5)
                ax1.add_patch(rect)
        
        # Add labels with more spacing
        ax1.text(-0.8, -0.8, "Ref:", ha='right', va='center', fontsize=12, fontweight='bold')
        ax1.text(-0.8, -1.2, "Status:", ha='right', va='center', fontsize=12, fontweight='bold')
        
        # Add legend subplot
        ax2 = plt.subplot2grid((5, 1), (4, 0))
        ax2.axis('off')
        
        # Create legend boxes with more spacing
        legend_x = 0.2  # Moved legend more to the left
        ax2.add_patch(plt.Rectangle((legend_x, 0.5), 0.1, 0.3, facecolor='#AAFFAA', alpha=0.7))
        ax2.text(legend_x + 0.15, 0.65, "Hit", va='center', fontsize=12)
        
        ax2.add_patch(plt.Rectangle((legend_x + 0.3, 0.5), 0.1, 0.3, facecolor='#FFAAAA', alpha=0.7))
        ax2.text(legend_x + 0.45, 0.65, "Fault", va='center', fontsize=12)
        
        # Add Second Chance specific legend
        if is_second_chance:
            ax2.text(legend_x + 0.7, 0.65, "★ = Second Chance (Ref bit = 1)", va='center', fontsize=12, color='#0000FF')
        
        # Set aspect ratio to be equal for main grid
        ax1.set_aspect('equal')
        
        # Adjust layout with more padding
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1, hspace=0.2)  # Increased hspace
        
        # Create canvas and add to widget
        canvas = FigureCanvas(fig)
        self.vm_visualization_widget.layout().addWidget(canvas)
        canvas.draw()

    def reset_vm(self):
        self.frames_input.clear()
        self.ref_input.clear()
        self.vm_results_text.clear()
        self.fifo_radio.setChecked(True)
        
        # Clear visualization
        for i in reversed(range(self.vm_visualization_widget.layout().count())): 
            self.vm_visualization_widget.layout().itemAt(i).widget().setParent(None)

    def run_ds_simulation(self):
        try:
            cylinders = int(self.cylinders_input.text())
            current_pos = int(self.current_pos_input.text())
            queue = [int(x.strip()) for x in self.queue_input.text().split(',')]
            
            if cylinders <= 0:
                raise ValueError("Number of cylinders must be positive")
            if current_pos < 0 or current_pos >= cylinders:
                raise ValueError("Current position must be between 0 and number of cylinders")
            if not all(0 <= x < cylinders for x in queue):
                raise ValueError("All queue values must be between 0 and number of cylinders")
            
            algorithm = "SCAN" if self.scan_radio.isChecked() else "LOOK"
            
            if algorithm == "SCAN":
                results = SCAN(cylinders, current_pos, queue)
            else:
                results = LOOK(cylinders, current_pos, queue)
            
            self.display_ds_results(results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))

    def display_ds_results(self, results):
        self.ds_results_text.clear()
        self.ds_results_text.append(f"Total Seek Distance: {results['total_distance']}")
        self.ds_results_text.append("Order of Served Requests:")
        self.ds_results_text.append(str(results['sequence']))
        
        self.visualize_ds_results(results)

    def visualize_ds_results(self, results):
        # Clear previous visualization
        for i in reversed(range(self.ds_visualization_widget.layout().count())): 
            self.ds_visualization_widget.layout().itemAt(i).widget().setParent(None)
        
        # Create new figure
        fig = plt.figure(figsize=(12, 6))
        canvas = FigureCanvas(fig)
        self.ds_visualization_widget.layout().addWidget(canvas)
        
        ax = fig.add_subplot(111)
        sequence = results['sequence']
        x = range(len(sequence))
        
        ax.plot(x, sequence, 'b-o')
        ax.set_xlabel('Step')
        ax.set_ylabel('Cylinder Position')
        ax.set_title('Disk Scheduling Sequence')
        ax.grid(True)
        
        canvas.draw()

    def reset_ds(self):
        self.cylinders_input.clear()
        self.current_pos_input.clear()
        self.queue_input.clear()
        self.ds_results_text.clear()
        self.scan_radio.setChecked(True)
        
        # Clear visualization
        for i in reversed(range(self.ds_visualization_widget.layout().count())): 
            self.ds_visualization_widget.layout().itemAt(i).widget().setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply material design theme
    apply_stylesheet(app, theme='light_blue.xml')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())