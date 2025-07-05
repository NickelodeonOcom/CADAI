
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from vedo.qt import QtViewer
from vedo import Text2D

class Viewport(QWidget):
    """
    A custom QWidget that embeds a vedo QtViewer.
    This is where the 3D scene is rendered.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.viewer = QtViewer(self)
        layout.addWidget(self.viewer)
        self.show_text("Welcome to CAD AI v2!\nDescribe objects to build a scene.")

    def display_assembly(self, assembly):
        """
        Clears the viewer and displays a new vedo Assembly object.
        
        Args:
            assembly (vedo.Assembly): The 3D scene to display.
        """
        self.viewer.clear()
        self.viewer.add(assembly)
        self.viewer.add_global_axes(axtype=1) # Add a small coordinate axis gizmo
        self.viewer.reset_camera()
        self.viewer.render()
        
    def show_text(self, text, c='black'):
        """
        Displays text in the center of the viewport.
        
        Args:
            text (str): The message to display.
            c (str): The color of the text.
        """
        self.viewer.clear()
        text_actor = Text2D(text, pos='center', c=c, font='Calco', s=1.2)
        self.viewer.add(text_actor)
        self.viewer.render()
