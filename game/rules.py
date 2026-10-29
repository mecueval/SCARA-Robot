# game/rules.py
import copy

def get_valid_moves(grid, player):
    """
    Escanea la matriz y devuelve todos los movimientos válidos para un jugador.
    Si hay una captura posible, prioriza devolver SOLO las capturas (obligatorio).
    """
    valid_moves = []
    valid_captures = []
    
    rows = len(grid)
    cols = len(grid[0])
    
    # 1. Definir dirección y oponente
    # El Robot (2) avanza hacia abajo (+1). Humano (1) hacia arriba (-1)
    direction = 1 if player == 2 else -1
    opponent = 1 if player == 2 else 2
    
    # 2. Escanear todo el tablero buscando las fichas del jugador
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == player:
                
                # Evaluar las dos diagonales posibles (Izquierda: -1, Derecha: +1)
                for d_col in [-1, 1]:
                    target_r = r + direction
                    target_c = c + d_col
                    
                    # Verificar que no nos salimos del tablero
                    if 0 <= target_r < rows and 0 <= target_c < cols:
                        
                        # CASO A: Movimiento simple (Casilla vacía)
                        if grid[target_r][target_c] == 0:
                            valid_moves.append({
                                'from': (r, c),
                                'to': (target_r, target_c),
                                'capture': None
                            })
                        
                        # CASO B: Salto / Captura (Ficha enemiga en frente)
                        elif grid[target_r][target_c] == opponent:
                            # Proyectar el salto (1 casilla más allá en la misma dirección)
                            jump_r = target_r + direction
                            jump_c = target_c + d_col
                            
                            # Verificar si la casilla de aterrizaje existe y está vacía
                            if 0 <= jump_r < rows and 0 <= jump_c < cols:
                                if grid[jump_r][jump_c] == 0:
                                    valid_captures.append({
                                        'from': (r, c),
                                        'to': (jump_r, jump_c),
                                        'capture': (target_r, target_c) # Ficha que será comida
                                    })
    

    return valid_moves + valid_captures


def apply_move(grid, move):
    """
    Toma un estado del tablero y aplica un movimiento.
    Retorna una NUEVA matriz (importante para que la IA pueda simular sin dañar el tablero real).
    """
    new_grid = copy.deepcopy(grid)
    
    orig_r, orig_c = move['from']
    dest_r, dest_c = move['to']
    
    # 1. Mover la ficha
    ficha = new_grid[orig_r][orig_c]
    new_grid[orig_r][orig_c] = 0
    new_grid[dest_r][dest_c] = ficha
    
    # 2. Eliminar la ficha si hubo captura
    if move['capture'] is not None:
        cap_r, cap_c = move['capture']
        new_grid[cap_r][cap_c] = 0
        
    return new_grid

def check_game_over(grid):
    """
    Árbitro del juego. Evalúa si el juego ha terminado.
    Retorna:
      0 = El juego continúa
      1 = Gana el Humano
      2 = Gana el Robot
      3 = Empate (Ambos bloqueados)
    """
    fichas_robot = 0
    fichas_humano = 0
    robot_en_meta = 0
    humano_en_meta = 0
    
    rows = len(grid)
    cols = len(grid[0])
    
    # 1. Contar fichas y revisar cuántas llegaron a la meta
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                fichas_robot += 1
                if r == rows - 1:  # Fila 7 (Meta del Robot)
                    robot_en_meta += 1
            elif grid[r][c] == 1:
                fichas_humano += 1
                if r == 0:         # Fila 0 (Meta del Humano)
                    humano_en_meta += 1
                    
    # CONDICIÓN A: Aniquilación total (Alguien se quedó sin fichas)
    if fichas_robot == 0: return 1
    if fichas_humano == 0: return 2
    
    # CONDICIÓN B (Tu regla): Todas las fichas supervivientes llegaron a la meta
    if fichas_robot > 0 and fichas_robot == robot_en_meta: return 2
    if fichas_humano > 0 and fichas_humano == humano_en_meta: return 1
    
    # CONDICIÓN C: Bloqueo (Alguien se quedó sin movimientos posibles)
    movs_robot = get_valid_moves(grid, 2)
    movs_humano = get_valid_moves(grid, 1)
    
    if not movs_robot and not movs_humano: return 3 # Empate técnico
    if not movs_robot: return 1 # El robot está acorralado, gana humano
    if not movs_humano: return 2 # El humano está acorralado, gana robot
    
    return 0 # Nadie ha ganado aún, el juego sigue