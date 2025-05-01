import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QScrollArea, 
                            QFrame, QLineEdit, QRadioButton, QButtonGroup,
                            QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
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
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("OS Algorithms Simulator")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Description
        desc = QLabel("Select the type of algorithm you want to simulate:")
        desc.setFont(QFont("Segoe UI", 12))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(desc)
        
        # Buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(20)
        
        # Virtual Memory button
        vm_button = QPushButton("Virtual Memory\nAlgorithms")
        vm_button.setFont(QFont("Segoe UI", 14))
        vm_button.setMinimumSize(200, 100)
        vm_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        vm_button.clicked.connect(self.open_virtual_memory)
        buttons_layout.addWidget(vm_button)
        
        # Disk Scheduling button
        ds_button = QPushButton("Disk Scheduling\nAlgorithms")
        ds_button.setFont(QFont("Segoe UI", 14))
        ds_button.setMinimumSize(200, 100)
        ds_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        ds_button.clicked.connect(self.open_disk_scheduling)
        buttons_layout.addWidget(ds_button)
        
        main_layout.addWidget(buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
    
    def open_virtual_memory(self):
        self.vm_window = VirtualMemoryWindow()
        self.vm_window.show()
    
    def open_disk_scheduling(self):
        self.ds_window = DiskSchedulingWindow()
        self.ds_window.show()

class VirtualMemoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Memory Algorithms")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
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
        self.run_button = QPushButton("Run Simulation")
        self.run_button.setFont(QFont("Segoe UI", 11))
        self.run_button.setStyleSheet("""
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
        self.run_button.clicked.connect(self.run_simulation)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Segoe UI", 11))
        self.reset_button.setStyleSheet("""
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
        self.reset_button.clicked.connect(self.reset)
        
        buttons_layout.addWidget(self.run_button)
        buttons_layout.addWidget(self.reset_button)
        content_layout.addLayout(buttons_layout)
        
        # Results area
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel("Results:")
        results_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        results_layout.addWidget(results_label)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        results_layout.addWidget(self.results_text)
        
        # Visualization area
        self.visualization_widget = QWidget()
        self.visualization_widget.setMinimumHeight(400)
        self.visualization_widget.setLayout(QVBoxLayout())  # Initialize layout
        results_layout.addWidget(self.visualization_widget)
        
        content_layout.addWidget(results_frame)
        
        # Set up scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def run_simulation(self):
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
            
            self.display_results(results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))
    
    def display_results(self, results):
        self.results_text.clear()
        self.results_text.append(f"Page Faults: {results['faults']}")
        self.results_text.append(f"Page Hits: {results['hits']}")
        self.results_text.append(f"Total References: {len(results['access_type'])}")
        self.results_text.append(f"Hit Rate: {(results['hits'] / len(results['access_type']) * 100):.1f}%")
        self.results_text.append(f"Fault Rate: {(results['faults'] / len(results['access_type']) * 100):.1f}%\n")
        self.results_text.append("Allocation Sequence:")
        
        for step in results['sequence']:
            self.results_text.append(str(step))
        
        self.visualize_results(results)
    
    def visualize_results(self, results):
        # Clear previous visualization
        for i in reversed(range(self.visualization_widget.layout().count())): 
            self.visualization_widget.layout().itemAt(i).widget().setParent(None)
        
        # Create new figure
        fig = plt.figure(figsize=(12, 6))
        canvas = FigureCanvas(fig)
        self.visualization_widget.layout().addWidget(canvas)
        
        ax = fig.add_subplot(111)
        sequence = results['sequence']
        
        # Get the full range of cylinders
        cylinders = int(self.frames_input.text())
        
        # Create positions list including 0 and max cylinder
        positions = sorted(set([0, cylinders - 1] + list(sequence)))
        x_positions = np.linspace(0, 1, len(positions))
        pos_to_x = dict(zip(positions, x_positions))
        
        # Add cylinder numbers at the top
        for pos, x in zip(positions, x_positions):
            ax.text(x, 1.1, str(pos), ha='center', va='bottom', color='orange', fontsize=10)
        
        # Plot the movement pattern
        x_coords = []
        y_coords = []
        y_spacing = 0.05  # Vertical spacing between points
        current_y = 0.8  # Starting y position
        
        # First point
        x_coords.append(pos_to_x[sequence[0]])
        y_coords.append(current_y)
        
        # Plot each segment
        for i in range(1, len(sequence)):
            current_y -= y_spacing
            x_coords.append(pos_to_x[sequence[i]])
            y_coords.append(current_y)
        
        # Plot lines and dots
        ax.plot(x_coords, y_coords, 'k-', linewidth=1)
        ax.plot(x_coords, y_coords, 'ko', markersize=8)
        
        # Clean up the plot
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Set view limits
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(0.2, 1.2)
        
        # Adjust layout
        plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
        
        canvas.draw()
    
    def reset(self):
        self.frames_input.clear()
        self.ref_input.clear()
        self.results_text.clear()
        self.fifo_radio.setChecked(True)
        
        # Clear visualization
        for i in reversed(range(self.visualization_widget.layout().count())): 
            self.visualization_widget.layout().itemAt(i).widget().setParent(None)

class DiskSchedulingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk Scheduling Algorithms")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
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
        self.run_button = QPushButton("Run Simulation")
        self.run_button.setFont(QFont("Segoe UI", 11))
        self.run_button.setStyleSheet("""
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
        self.run_button.clicked.connect(self.run_simulation)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Segoe UI", 11))
        self.reset_button.setStyleSheet("""
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
        self.reset_button.clicked.connect(self.reset)
        
        buttons_layout.addWidget(self.run_button)
        buttons_layout.addWidget(self.reset_button)
        content_layout.addLayout(buttons_layout)
        
        # Results area
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel("Results:")
        results_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        results_layout.addWidget(results_label)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        results_layout.addWidget(self.results_text)
        
        # Visualization area
        self.visualization_widget = QWidget()
        self.visualization_widget.setMinimumHeight(400)
        self.visualization_widget.setLayout(QVBoxLayout())  # Initialize layout
        results_layout.addWidget(self.visualization_widget)
        
        content_layout.addWidget(results_frame)
        
        # Set up scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def run_simulation(self):
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
            
            self.display_results(results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))
    
    def display_results(self, results):
        self.results_text.clear()
        self.results_text.append(f"Total Seek Distance: {results['total_distance']}")
        self.results_text.append("Order of Served Requests:")
        self.results_text.append(str(results['sequence']))
        
        self.visualize_results(results)
    
    def visualize_results(self, results):
        # Clear previous visualization
        for i in reversed(range(self.visualization_widget.layout().count())): 
            self.visualization_widget.layout().itemAt(i).widget().setParent(None)
        
        # Create new figure
        fig = plt.figure(figsize=(12, 6))
        canvas = FigureCanvas(fig)
        self.visualization_widget.layout().addWidget(canvas)
        
        ax = fig.add_subplot(111)
        sequence = results['sequence']
        
        # Get the full range of cylinders
        cylinders = int(self.cylinders_input.text())
        
        # Create positions list including 0 and max cylinder
        positions = sorted(set([0, cylinders - 1] + list(sequence)))
        x_positions = np.linspace(0, 1, len(positions))
        pos_to_x = dict(zip(positions, x_positions))
        
        # Add cylinder numbers at the top
        for pos, x in zip(positions, x_positions):
            ax.text(x, 1.1, str(pos), ha='center', va='bottom', color='orange', fontsize=10)
        
        # Plot the movement pattern
        x_coords = []
        y_coords = []
        y_spacing = 0.05  # Vertical spacing between points
        current_y = 0.8  # Starting y position
        
        # First point
        x_coords.append(pos_to_x[sequence[0]])
        y_coords.append(current_y)
        
        # Plot each segment
        for i in range(1, len(sequence)):
            current_y -= y_spacing
            x_coords.append(pos_to_x[sequence[i]])
            y_coords.append(current_y)
        
        # Plot lines and dots
        ax.plot(x_coords, y_coords, 'k-', linewidth=1)
        ax.plot(x_coords, y_coords, 'ko', markersize=8)
        
        # Clean up the plot
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Set view limits
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(0.2, 1.2)
        
        # Adjust layout
        plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
        
        canvas.draw()
    
    def reset(self):
        self.cylinders_input.clear()
        self.current_pos_input.clear()
        self.queue_input.clear()
        self.results_text.clear()
        self.scan_radio.setChecked(True)
        
        # Clear visualization
        for i in reversed(range(self.visualization_widget.layout().count())): 
            self.visualization_widget.layout().itemAt(i).widget().setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply material design theme
    apply_stylesheet(app, theme='light_blue.xml')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
