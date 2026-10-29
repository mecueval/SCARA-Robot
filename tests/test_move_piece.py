# test/test_move_piece.py
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from hardware.robot_arm import RobotArm
from game.board import SimpleCheckers

def test_move_piece():
    print("\n" + "="*60)
    print("   INTEGRACIÓN: SCARA + LÓGICA DE DAMAS (PICK & PLACE)")
    print("="*60)

    # 1. Inicializar Hardware y Juego
    brazo = RobotArm(config)
    juego = SimpleCheckers(config)
    
    # Alturas de seguridad para el eje Z (Asumiendo que Pz = 20 es el nivel de la ficha)
    Z_HOVER = config.BOARD_OFFSET_Z + 30.0  # 30 mm sobre el tablero para no chocar
    Z_TABLERO = config.BOARD_OFFSET_Z       # Altura para agarrar/soltar la ficha

    # 2. Definir el movimiento lógico (El Robot mueve de [1][2] a [2][3])
    origen_row, origen_col = 1, 2
    destino_row, destino_col = 2, 3

    print(f"\n[COMANDO] Mover ficha de [{origen_row}][{origen_col}] hacia [{destino_row}][{destino_col}]")

    # 3. Traducir a milímetros reales
    orig_X, orig_Y = juego.get_physical_coordinates(origen_row, origen_col)
    dest_X, dest_Y = juego.get_physical_coordinates(destino_row, destino_col)

    print(f" -> Origen Físico : X={orig_X:.1f}, Y={orig_Y:.1f}")
    print(f" -> Destino Físico: X={dest_X:.1f}, Y={dest_Y:.1f}")

    # ==========================================
    # SECUENCIA FÍSICA DE MOVIMIENTO
    # ==========================================

    # PASO 1: Viajar sobre la casilla de origen (Hover)
    print("\n[SECUENCIA 1] Viajando a la casilla de origen...")
    brazo.move_linear(orig_X, orig_Y, Z_HOVER, steps=10, verbose=True)

    # PASO 2: Bajar a agarrar la ficha
    print("\n[SECUENCIA 2] Bajando el eje Z para agarrar la ficha...")
    # Aquí iría el código de tu motor Z o servo
    time.sleep(1) # Simulamos el tiempo de bajada
    print(" -> (CLIC) Efector final encendido. Ficha asegurada.")

    # PASO 3: Subir con la ficha
    print("\n[SECUENCIA 3] Levantando la ficha...")
    # Aquí iría el código para subir el Z
    time.sleep(1)

    # PASO 4: Viajar a la casilla de destino (Hover)
    print("\n[SECUENCIA 4] Viajando a la casilla de destino con la ficha...")
    brazo.move_linear(dest_X, dest_Y, Z_HOVER, steps=10, verbose=True)

    # PASO 5: Bajar a soltar la ficha
    print("\n[SECUENCIA 5] Bajando el eje Z para soltar la ficha...")
    time.sleep(1)
    print(" -> (CLIC) Efector final apagado. Ficha colocada.")

    # PASO 6: Subir y volver a Home
    print("\n[SECUENCIA 6] Retirando el brazo y volviendo a Home...")
    time.sleep(1)
    brazo.move_linear(100.0, 0.0, Z_HOVER, steps=10)

    print("\n[ÉXITO] Movimiento de Pick & Place completado.")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_move_piece()