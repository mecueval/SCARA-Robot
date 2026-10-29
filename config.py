# config.py

# Longitud de los eslabones del SCARA (en milímetros)
L1 = 150.0  # Altura estructurabase
L2 = 130.0  # Longitud del primer brazo horizonal
L3 = 130.0  # Longitud del segundo brazo

# Configuración del tablero (relativo al centro de la base del robot)
# Asumimos que el tablero empieza a 80 mm frente al robot en el eje X
BOARD_OFFSET_X = 80.0
BOARD_OFFSET_Y = 0.0
BOARD_OFFSET_Z = 20.0

SQUARE_SIZE = 20.0  # Tamaño de cada casilla en mm

# ==========================================
# CONFIGURACIÓN DE MOTORES Y PINES (Raspberry Pi 5)
# ==========================================
# Motor 1 (Hombro / q1)
PIN_DIR_1 = 20
PIN_STEP_1 = 21

# Motor 2 (Codo / q2)
PIN_DIR_2 = 22
PIN_STEP_2 = 23

# Configuración física de los NEMA 17
STEPS_PER_REV = 200    # NEMA 17 estándar (1.8 grados por paso)
MICROSTEPPING = 16     # Configuración del A4988 (1/16 suele ser el estándar)
GEAR_RATIO = 3.0       # Relación de poleas (Ej. 60 dientes / 20 dientes = 3). Pon 1.0 si es acople directo.

# ==========================================
# CONFIGURACIÓN DEL JUEGO (DAMAS)
# ==========================================
BOARD_ROWS = 8
BOARD_COLS = 8