from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QFileDialog, 
                             QListWidget, QFrame)
from PyQt6.QtGui import QFont
from vedo import Assembly
from gui.viewport import Viewport
from nlp.parser import parse_command
from geometry.generator import generate_and_add_to_scene
from exporter.file_exporter import export_model

class MainWindow(QMainWindow):
    """
    The main window of the application, version 3.
    Connects to the new AI parser and procedural geometry engine.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAD AI v3 - Procedural Engine")
        self.setGeometry(100, 100, 1600, 900)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Left Panel (Controls & Scene Graph) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(400)

        # Input text area
        self.label = QLabel("Describe the objects you want to create:")
        self.label.setFont(QFont("Arial", 12))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Try advanced shapes!\n\n"
            "e.g., 'Create a gear with 24 teeth, an inner radius of 4 and an outer radius of 5.'\n\n"
            "e.g., 'A wooden barrel at 5 0 0.'\n\n"
            "e.g., 'A red cube with side 4 at -5 0 0.'"
        )
        self.text_input.setMinimumHeight(150)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Add to Scene")
        self.generate_button.clicked.connect(self.add_to_scene)
        self.clear_button = QPushButton("Clear Scene")
        self.clear_button.clicked.connect(self.clear_scene)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.clear_button)

        # Scene Graph
        self.scene_label = QLabel("Scene Objects:")
        self.scene_label.setFont(QFont("Arial", 12))
        self.scene_list = QListWidget()
        
        # Export button
        self.export_button = QPushButton("Export Scene")
        self.export_button.clicked.connect(self.export_scene)
        self.export_button.setEnabled(False)

        # Assemble left panel
        left_layout.addWidget(self.label)
        left_layout.addWidget(self.text_input)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.scene_label)
        left_layout.addWidget(self.scene_list)
        left_layout.addWidget(self.export_button)

        # --- Right Panel (3D Viewport) ---
        self.viewport = Viewport()

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.viewport, 1)

        # Initialize scene
        self.clear_scene()

    def add_to_scene(self):
        """
        Takes user text, parses it with the AI parser, generates geometry, and adds it to the scene.
        """
        input_text = self.text_input.toPlainText()
        if not input_text:
            return

        try:
            commands = parse_command(input_text)
            if not commands:
                raise ValueError("Could not find any valid objects to create.")
            
            generate_and_add_to_scene(commands, self.scene_assembly)
            
            self.viewport.display_assembly(self.scene_assembly)
            self.update_scene_list()
            self.export_button.setEnabled(self.scene_assembly.npoints > 0)
            self.text_input.clear()

        except ValueError as e:
            print(f"Error: {e}")
            self.viewport.show_text(f"Error:\n{e}", c='red')

    def clear_scene(self):
        self.scene_assembly = Assembly()
        self.viewport.display_assembly(self.scene_assembly)
        self.update_scene_list()
        self.export_button.setEnabled(False)
        
    def update_scene_list(self):
        self.scene_list.clear()
        for i, mesh in enumerate(self.scene_assembly.unpack()):
            name = mesh.name if mesh.name else f"Object_{i+1}"
            self.scene_list.addItem(name)

    def export_scene(self):
        if not self.scene_assembly.unpack():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Scene", "", "STL Files (*.stl);;OBJ Files (*.obj);;VTK Files (*.vtk);;All Files (*)"
        )
        if file_path:
            export_model(self.scene_assembly, file_path)
