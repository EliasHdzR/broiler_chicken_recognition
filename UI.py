from PyQt6.QtCore import QSize, pyqtSlot as Slot
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from Utils.VideoPlayer import VideoPlayer
from Utils.VideoProcessor import VideoProcessor
from Utils.VideoThread import VideoThread

class Window(QWidget):
    def __init__(self):
        # variables
        self.videoProcessor = None
        self.video_path = None

        super().__init__()
        self.setWindowTitle("Pigeon Detector")
        self.setGeometry(100, 100, self.minimumWidth(), 600)

        self.buttonOpen = QPushButton("Cargar Video")
        BUTTON_SIZE = QSize(200, 50)
        self.buttonOpen.setMinimumSize(BUTTON_SIZE)
        self.buttonOpen.clicked.connect(self.HandleOpen)

        self.buttonProcess = QPushButton("Analizar Video")
        self.buttonProcess.setMinimumSize(BUTTON_SIZE)
        self.buttonProcess.clicked.connect(self.ProcessImage)

        self.videoPlayer = VideoPlayer()
        self.videoThread = None

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.buttonOpen)
        btnLayout.addWidget(self.buttonProcess)

        layout = QVBoxLayout(self)
        layout.addLayout(btnLayout)
        layout.addWidget(self.videoPlayer)

    def HandleOpen(self):
        """
        Abre el dialogo para seleccionar un video
        """
        start = "./resources"
        path = QFileDialog.getOpenFileName(self, "Choose File", start, "Videos(*.mp4)")[0]
        if path == "": return

        if self.videoProcessor is not None and self.videoProcessor.isRunning():
            self.videoProcessor.stop()

        if self.videoThread is not None and self.videoThread.isRunning():
            self.videoThread.stop()

        self.video_path = path

        self.videoThread = VideoThread(self.video_path)
        self.videoThread.frame_signal.connect(self.setImage)
        self.videoThread.start()

    def ProcessImage(self):
        """
        Inicia el procesamiento del video
        :return:
        """
        if self.video_path is not None:
            self.videoThread.stop()
            self.videoProcessor = VideoProcessor(self.video_path)
            self.videoProcessor.frame_signal.connect(self.setImage)
            self.videoProcessor.start()

    @Slot(QImage)
    def setImage(self, image):
        """
        Función que recibe una imagen de un hilo y la muestra en un WebCamLabel.
        :param image: Imagen a mostrar.
        :return:
        """
        pixmap = QPixmap.fromImage(image)
        self.videoPlayer.setPixmap(pixmap)