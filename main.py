# main.py
import time
import sys

import config
from hardware.robot_arm import RobotArm
from game.board import SimpleCheckers
from game.rules import get_valid_moves, apply_move, check_game_over
from game.ai import get_best_move

def execute_physical_move(arm, board, move):
    """
    Traduce el diccionario lógico del movimiento en comandos físicos para el SCARA.
    """
    Z_HOVER = config.BOARD_OFFSET_Z + 30.0
    
    # 1. MOVER LA FICHA PRINCIPAL
    orig_r, orig_c = move['from']
    dest_r, dest_c = move['to']
    
    orig_x, orig_y = board.get_physical_coordinates(orig_r, orig_c)
    dest_x, dest_y = board.get_physical_coordinates(dest_r, dest_c)
    
    print("\n[ROBOT] Ejecutando Pick & Place...")
    arm.move_linear(orig_x, orig_y, Z_HOVER, steps=15)
    print(" -> Bajando eje Z y agarrando ficha...")
    time.sleep(1) # Simulación de actuador
    
    arm.move_linear(dest_x, dest_y, Z_HOVER, steps=15)
    print(" -> Bajando eje Z y soltando ficha...")
    time.sleep(1) # Simulación de actuador
    
    # 2. RETIRAR FICHA ENEMIGA (Si hubo captura)
    if move['capture']:
        cap_r, cap_c = move['capture']
        cap_x, cap_y = board.get_physical_coordinates(cap_r, cap_c)
        
        print("\n[ROBOT] Retirando ficha humana capturada...")
        arm.move_linear(cap_x, cap_y, Z_HOVER, steps=15)
        print(" -> Agarrando ficha capturada...")
        time.sleep(1)
        
        # Llevar la ficha fuera del tablero (Zona de "Basura")
        arm.move_linear(80.0, 100.0, Z_HOVER, steps=15) 
        print(" -> Soltando ficha fuera del tablero.")
        time.sleep(1)

    # 3. VOLVER A HOME
    arm.move_linear(100.0, 0.0, Z_HOVER, steps=15)


def get_human_move(grid):
    """
    Pide al humano que ingrese su movimiento por consola y lo valida.
    """
    movimientos_validos = get_valid_moves(grid, player=1)
    
    while True:
        try:
            print("\nTus movimientos válidos (Formato: Fila,Columna):")
            for i, mov in enumerate(movimientos_validos):
                cap_msg = f" (¡COME LA FICHA EN {mov['capture']}!)" if mov['capture'] else ""
                print(f"  {i}: De {mov['from']} hacia {mov['to']}{cap_msg}")
                
            eleccion = int(input("\nElige el número de tu movimiento: "))
            
            if 0 <= eleccion < len(movimientos_validos):
                return movimientos_validos[eleccion]
            else:
                print("Número fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")


def main():
    print("="*60)
    print("       SCARA CHECKERS - INICIANDO SISTEMA")
    print("="*60)
    
    # Inicializar hardware y juego
    arm = RobotArm(config)
    juego = SimpleCheckers(config)
    turno_actual = 1 # 1 = Humano (H), 2 = Robot (R)
    
    while True:
        # 1. Mostrar estado del juego
        juego.print_board()
        
        # 2. Revisar si alguien ganó
        estado = check_game_over(juego.grid)
        if estado == 1:
            print("\n🏆 ¡EL HUMANO HA GANADO LA PARTIDA! 🏆")
            break
        elif estado == 2:
            print("\n🤖 ¡EL ROBOT HA GANADO LA PARTIDA! 🤖")
            break
        elif estado == 3:
            print("\n🤝 EMPATE TÉCNICO. Nadie puede moverse. 🤝")
            break
            
        # 3. Turno del Jugador
        if turno_actual == 1:
            print("\n--- TURNO DEL HUMANO (H) ---")
            movimiento = get_human_move(juego.grid)
            
            # Aplicar en la matriz lógica (el humano mueve la ficha con su propia mano)
            juego.grid = apply_move(juego.grid, movimiento)
            
            # Pausa para que el humano saque su mano del tablero
            input("Presiona [ENTER] cuando hayas movido físicamente tu ficha...")
            turno_actual = 2
            
        # 4. Turno del Robot
        else:
            print("\n--- TURNO DEL ROBOT (R) ---")
            print("El Robot está pensando su jugada (Minimax)...")
            
            # La IA elige la mejor jugada
            mejor_movimiento = get_best_move(juego.grid, depth=3)
            
            orig = mejor_movimiento['from']
            dest = mejor_movimiento['to']
            print(f"Decisión de la IA: Mover de {orig} hacia {dest}")
            
            # Ejecutar hardware
            execute_physical_move(arm, juego, mejor_movimiento)
            
            # Actualizar matriz lógica
            juego.grid = apply_move(juego.grid, mejor_movimiento)
            turno_actual = 1

if __name__ == "__main__":
    main()