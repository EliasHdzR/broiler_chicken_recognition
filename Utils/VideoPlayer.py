from PyQt6.QtWidgets import QLabel

class VideoPlayer(QLabel):
    """
    Clase que representa un QLabel para mostrar la imagen del video
    """

    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setStyleSheet("border: 1px solid black;")