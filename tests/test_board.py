# test/test_board.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from game.board import SimpleCheckers

def test_game_board():
    print("--- INICIANDO PRUEBA DEL TABLERO DE JUEGO ---")
    
    # 1. Inicializar el juego
    juego = SimpleCheckers(config)
    
    # 2. Imprimir cómo se ve el tablero virtual
    juego.print_board()
    
    # 3. Probar la traducción de coordenadas en puntos extremos
    puntos_prueba = [
        (0, 0, "Esquina Inferior Derecha (Cerca del robot)"),
        (0, 7, "Esquina Inferior Izquierda (Cerca del robot)"),
        (7, 0, "Esquina Superior Derecha (Lejos del robot)"),
        (7, 7, "Esquina Superior Izquierda (Lejos del robot)"),
        (3, 3, "Centro del tablero (Casilla vacía)"),
    ]
    
    print("--- MAPEO A COORDENADAS CARTESIANAS ---")
    print(f"Tamaño de casilla: {config.SQUARE_SIZE} mm")
    print(f"Offset X del tablero: {config.BOARD_OFFSET_X} mm\n")
    
    for row, col, desc in puntos_prueba:
        px, py = juego.get_physical_coordinates(row, col)
        print(f"[{row}][{col}] {desc:<42} -> X: {px:>5.1f} mm, Y: {py:>5.1f} mm")

if __name__ == "__main__":
    test_game_board()