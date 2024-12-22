import cv2
import time
import os

# Crear un directorio para guardar las capturas
output_dir = "capturas"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Capturar video desde un dispositivo de captura (generalmente ID 0 o 1)
video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not video_capture.isOpened():
    print("No se pudo acceder al dispositivo de captura.")
    exit()

print("Presiona 'q' para salir.")

# Contador para las imágenes
frame_count = 0

# Bucle para mostrar el video y capturar cada 5 segundos
last_capture_time = time.time()

while True:
    ret, frame = video_capture.read()
    if ret:
        # Mostrar el video en la ventana
        cv2.imshow("Monitor Output", frame)

        # Capturar cada 5 segundos
        current_time = time.time()
        if current_time - last_capture_time >= 5:
            frame_count += 1
            filename = os.path.join(output_dir, f"captura_{frame_count:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captura guardada: {filename}")
            last_capture_time = current_time

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
