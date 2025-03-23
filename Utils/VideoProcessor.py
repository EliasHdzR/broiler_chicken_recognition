import cv2
from ultralytics import YOLO
from PyQt6.QtCore import QThread, pyqtSignal as Signal
from PyQt6.QtGui import QImage
from Utils.CVtoQtImage import cvimage_to_qimage
import time

class VideoProcessor(QThread):
    frame_signal = Signal(QImage)

    def __init__(self, video_path):
        super().__init__()
        self.model = YOLO("Utils/best.pt")
        self.running = True
        self.video_path = video_path

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

            results = self.model(frame)
            pigeon_count = 0

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    score = box.conf[0].item()
                    label = f"Paloma {score:.2f}"

                    if score > 0.95:
                        pigeon_count += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 255, 0), 1, cv2.LINE_AA)

            cv2.putText(frame, f"Palomas detectadas: {pigeon_count}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
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