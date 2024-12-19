# pylint: disable=no-member
import cv2
from detectar_figura.detector_figura import on_trackbar_change, detect_shapes_in_image, fill_cells, highlight_start_end
from laberinto.laberinto import draw_grid, maze_generate
from movimiento_robot.mover_robot import mover_robot
from qLearning.Q_learning import aplicarQlearning
from sarsa.Sarsa import aplicarSarsa
from generar_graficas.grafico_entrenamiento import graficar_entrenamiento
import requests
# URL de DroidCam
url = "http://192.168.1.8:4747/video"
server_url="http://192.168.1.4:5000"

# Parámetros de la cuadrícula
rows = 5 # Número de filas
cols = 5  # Número de columnas
thickness = 1  # Grosor de las líneas
count = 0

# Valores iniciales de Canny
canny_threshold1 = 50
canny_threshold2 = 150

politica = {0: [0,0,0,1],
            1: [0,0,0,1],
            2: [0,1,0,0],
            3: [0,1,0,0],
            4: [0,0,0,0],
            5: [0,1,0,0],
            6: [0,0,0,1],
            7: [0,0,0,1],
            8: [0,0,0,0],
            }



# Abre el video desde la URL
cap = cv2.VideoCapture(url)
#cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo conectar a la cámara en la URL proporcionada.")
else:
    print(f"Conexión exitosa. Analizando video con cuadrícula de {rows}x{cols}...")

    # Crear ventana y trackbars
    cv2.namedWindow('Ajustes')
    cv2.createTrackbar('Canny Th1', 'Ajustes', canny_threshold1, 255, on_trackbar_change)
    cv2.createTrackbar('Canny Th2', 'Ajustes', canny_threshold2, 255, on_trackbar_change)
    cv2.createTrackbar('Dilatacion', 'Ajustes', 2, 15, on_trackbar_change)
    # Llama al endpoint para obtener el laberinto
 # Llama al endpoint para obtener el laberinto
    #try:
    response_maze = requests.get(f"{server_url}/maze", timeout=25)  # Llamada con timeout
    response_maze.raise_for_status()  # Lanza una excepción si hay un código de error HTTP
    maze = response_maze.json()  # Asume que el endpoint devuelve un JSON representando el maze
    print("Laberinto recibido del servidor:", maze)
    # except requests.exceptions.RequestException as e:
    #  print(f"Error al obtener el laberinto desde el servidor: {e}")
    # Usa un respaldo local si el servidor falla 
    #maze = maze_generate(rows, cols)
    
    #maze = maze_generate(rows, cols)
    #maze = [[0,0,0],
    #        [0,1,0], 
    #        [0,0,0]]

    tablaQ, retorno_qLearning = aplicarSarsa(maze)
    #aplicarQlearning(maze)
    print("dsasddasd____________",tablaQ)
    
    qr_detector = cv2.QRCodeDetector()
    while True:
        count += 4
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el video.")
            break

        # Obtener valores de las trackbars
        threshold1 = cv2.getTrackbarPos('Canny Th1', 'Ajustes')
        threshold2 = cv2.getTrackbarPos('Canny Th2', 'Ajustes')
        dilatacion = cv2.getTrackbarPos('Dilatacion', 'Ajustes')

        # Analizar el frame con los umbrales ajustados
        detected_shapes, frame_with_shapes = detect_shapes_in_image(frame, rows, cols, qr_detector)
        
        #detected_shapes=[{"shape": "triangle","row":1,"col": 0,"cell_index": 3,"x": 100,"y": 100}]
        #moverRobot(tablaQ,cell_index,x,y)
        print(detected_shapes)
        # Dibujar la cuadrícula en el frame
        frame_with_grid = draw_grid(frame_with_shapes, rows, cols, thickness)

        frame=fill_cells(frame_with_grid,maze)
        frame = highlight_start_end(frame, rows, cols)
        # Mostrar el frame con los ajustes
        cv2.imshow('Cuadrícula con análisis', frame_with_grid)

        if count % 24 == 0:
            print("Enviando comando")
            #comunicacionArduino.send_command("w")
            mover_robot(tablaQ, detected_shapes)

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

        

# Libera recursos
cap.release()
cv2.destroyAllWindows()
