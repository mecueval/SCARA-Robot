# test/test_ai.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.ai import get_best_move
from game.rules import get_valid_moves

def print_grid(grid):
    cols = len(grid[0])
    print("    " + "   ".join([str(c) for c in range(cols)]))
    print("  +" + "---+" * cols)
    for r in range(len(grid)):
        row_str = f"{r} |"
        for c in range(cols):
            val = grid[r][c]
            char = " "
            if val == 1: char = "H"
            if val == 2: char = "R"
            row_str += f" {char} |"
        print(row_str)
        print("  +" + "---+" * cols)
    print()

def test_ai_decision():
    print("\n--- TEST: INTELIGENCIA ARTIFICIAL (MINIMAX) ---")
    
    grid = [[0 for _ in range(8)] for _ in range(8)]
    
    # LA TRAMPA EN EL CENTRO (Sin paredes para esconderse)
    grid[2][2] = 2  # Ficha Robot 1 (En peligro de muerte si avanza)
    grid[2][6] = 2  # Ficha Robot 2 (Totalmente a salvo)
    
    grid[4][2] = 1  # Ficha Humana (Cazador)
    
    print("\n[ESCENARIO TÁCTICO MEJORADO]")
    print("-> El Robot tiene la ficha [2][2].")
    print("-> Si el Robot la mueve a [3][1] o [3][3], el Humano en [4][2] la saltará y se la comerá.")
    print("-> ¡No hay paredes para esconderse! Debe mover la ficha segura en [2][6].")
    
    print("\n[ESTADO DEL TABLERO]")
    print_grid(grid)
    
    movimientos_posibles = get_valid_moves(grid, player=2)
    print(f"Opciones totales para el Robot: {len(movimientos_posibles)}")
    for i, m in enumerate(movimientos_posibles):
        print(f"  Opción: Mover de {m['from']} a {m['to']}")
        
    print("\n[IA PENSANDO (Minimax Depth=3)...]")
    mejor_movimiento = get_best_move(grid, depth=3)
    
    print(f"\n[DECISIÓN DE LA IA]")
    print(f"El Robot decidió mover de {mejor_movimiento['from']} hacia {mejor_movimiento['to']}")
    
    if mejor_movimiento['from'] == (2, 6):
        print("-> ¡ÉXITO! La IA detectó la trampa central, evitó el suicidio y jugó seguro.")
    else:
        print("-> ERROR: La IA cayó en la trampa.")

if __name__ == "__main__":
    test_ai_decision()