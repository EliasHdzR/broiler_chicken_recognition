import time
import cv2
from PyQt6.QtCore import QThread, pyqtSignal as Signal
from PyQt6.QtGui import QImage
from Utils.CVtoQtImage import cvimage_to_qimage

class VideoThread(QThread):
    frame_signal = Signal(QImage)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error al abrir el video: {self.video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1.0 / fps

        while self.running and cap.isOpened():
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                break

            image = cvimage_to_qimage(frame)
            self.frame_signal.emit(image)

            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed_time)
            time.sleep(sleep_time)

        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

    def isRunning(self):
        return self.running