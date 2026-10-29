# test/test_rules.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.rules import get_valid_moves, apply_move

def print_grid(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    print("    " + "   ".join([str(c) for c in range(cols)]))
    print("  +" + "---+" * cols)
    for r in range(rows):
        row_str = f"{r} |"
        for c in range(cols):
            val = grid[r][c]
            char = " "
            if val == 1: char = "H" # Humano
            if val == 2: char = "R" # Robot
            row_str += f" {char} |"
        print(row_str)
        print("  +" + "---+" * cols)
    print()

def test_game_rules():
    print("\n--- TEST: MOTOR DE REGLAS (DAMAS) ---")
    
    # Crear un tablero vacío manualmente
    grid = [[0 for _ in range(8)] for _ in range(8)]
    
    # Colocar fichas para crear un escenario de salto
    grid[2][3] = 2  # Ficha del Robot
    grid[3][4] = 1  # Ficha del Humano (Puesta para ser comida)
    grid[3][2] = 0  # Espacio libre a la izquierda (movimiento simple)
    
    print("\n[ESTADO INICIAL DEL TABLERO]")
    print_grid(grid)
    
    # 1. Analizar movimientos del Robot
    print("[ANALIZANDO MOVIMIENTOS PARA EL ROBOT (2)]")
    movimientos = get_valid_moves(grid, player=2)
    
    for idx, mov in enumerate(movimientos):
        origen = mov['from']
        destino = mov['to']
        captura = mov['capture']
        
        if captura:
            print(f"Opción {idx+1}: SALTO OBLIGATORIO desde {origen} hacia {destino}. (Comerá la ficha en {captura})")
        else:
            print(f"Opción {idx+1}: Movimiento simple desde {origen} hacia {destino}.")
            
    # 2. Aplicar el primer movimiento encontrado
    if movimientos:
        print("\n[APLICANDO EL MEJOR MOVIMIENTO...]")
        nuevo_tablero = apply_move(grid, movimientos[0])
        print_grid(nuevo_tablero)
        
        if movimientos[0]['capture']:
            print("¡El robot ha capturado la ficha humana y aterrizado con éxito!")

if __name__ == "__main__":
    test_game_rules()