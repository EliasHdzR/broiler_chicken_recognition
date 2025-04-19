import cv2
import os

def extraer_fotogramas(video_ruta, carpeta_salida):
    # Verifica si la carpeta de salida existe, si no, la crea
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Captura el video
    video = cv2.VideoCapture(video_ruta)
    contador = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break  # Sale cuando ya no hay más fotogramas

        # Guarda el fotograma
        nombre_fotograma = os.path.join(carpeta_salida, f"frame_{contador:05d}.jpg")
        cv2.imwrite(nombre_fotograma, frame)
        contador += 1

    # Libera el video
    video.release()
    print(f"Se han extraído {contador} fotogramas en {carpeta_salida}")

# Ejemplo de uso
ruta_video = "/home/eliash/Descargas/pollos_4.mp4"  # Reemplaza con la ruta de tu video
carpeta_destino = "/home/eliash/Descargas/pollos_4"
extraer_fotogramas(ruta_video, carpeta_destino)
