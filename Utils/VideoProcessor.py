import cv2
from ultralytics import YOLO
from PyQt6.QtCore import QThread, pyqtSignal as Signal
from PyQt6.QtGui import QImage
from Utils.CVtoQtImage import cvimage_to_qimage
import time

class VideoProcessor(QThread):
    """
    Clase que procesa un video y detecta palomas
    """
    frame_signal = Signal(QImage)

    def __init__(self, video_path):
        super().__init__()
        self.model = YOLO("Utils/best.pt")
        self.running = True
        self.video_path = video_path

    def run(self):
        """
        Procesa un archivo de vídeo fotograma a fotograma, realiza la detección de objetos utilizando un modelo
        preentrenado en cada fotograma y emite el fotograma procesado con anotaciones visuales.

        Para cada fotograma se crean cuadros delimitadores para las detecciones
        que superan un umbral de confianza del 50 % y el recuento de detecciones se muestra en el fotograma.
        Los fotogramas procesados se convierten al formato QImage y se emiten mediante una señal para su uso posterior.
        """

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

            results = self.model(frame)
            pollo_count = 0

            # Dibujar las cajas de los pollos detectadas con más de un 50% de certeza
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    score = box.conf[0].item()
                    label = f"Pollo {score:.2f}"

                    if score > 0.50:
                        pollo_count += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 255, 0), 1, cv2.LINE_AA)

            cv2.putText(frame, f"Pollos detectados: {pollo_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
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