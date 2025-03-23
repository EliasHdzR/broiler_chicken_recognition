import cv2
from PyQt6.QtGui import QImage

def cvimage_to_qimage(frame):
    height, width, channel = frame.shape
    bytes_per_line = 3 * width
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)