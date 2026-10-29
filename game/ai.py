from game.rules import get_valid_moves, apply_move, check_game_over

def evaluate_board(grid):
    """
    Función Heurística con Instinto Asesino.
    """
    # 1. Primero, preguntamos al árbitro si este tablero es una victoria definitiva
    estado = check_game_over(grid)
    if estado == 2: return 1000000   # ¡El Robot Gana! (Premio infinito)
    if estado == 1: return -1000000  # ¡El Robot Pierde! (Castigo infinito)
    if estado == 3: return 0         # Empate
    
    # 2. Si el juego sigue, evaluamos la táctica normal
    score = 0
    rows = len(grid)
    
    for r in range(rows):
        for c in range(len(grid[0])):
            if grid[r][c] == 2:
                score += 10      # Supervivencia
                score += r       # Avance hacia la meta
            elif grid[r][c] == 1:
                score -= 10
                score -= (rows - 1 - r)
                
    return score

def minimax(grid, depth, maximizing_player):
    """
    Algoritmo Minimax para explorar el árbol de decisiones.
    - depth: Cuántos turnos hacia el futuro va a simular.
    - maximizing_player: True si es turno del Robot, False si es del Humano.
    """
    # Condición de parada: Llegamos al límite de predicción
    if depth == 0:
        return evaluate_board(grid)
        
    # Definir de quién es el turno en esta simulación
    player = 2 if maximizing_player else 1
    moves = get_valid_moves(grid, player)
    
    # Si alguien se queda sin movimientos, el juego termina
    if not moves:
        return evaluate_board(grid)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            # Imaginar el tablero futuro si hacemos este movimiento
            future_grid = apply_move(grid, move)
            # Llamar recursivamente a Minimax (ahora es turno del humano)
            eval = minimax(future_grid, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
        
    else:
        min_eval = float('inf')
        for move in moves:
            # Imaginar el tablero futuro si el humano hace este movimiento
            future_grid = apply_move(grid, move)
            # Llamar recursivamente (ahora es turno del robot de nuevo)
            eval = minimax(future_grid, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(grid, depth=3):
    """
    Evalúa todos los movimientos iniciales posibles y elige el que 
    tenga la mejor puntuación según Minimax.
    """
    best_move = None
    max_eval = float('-inf')
    
    # Obtener qué movimientos reales puede hacer el robot hoy
    moves = get_valid_moves(grid, player=2)
    
    # Si hay un salto obligatorio, las reglas ya lo filtraron.
    # Si solo hay 1 movimiento posible, no perdemos tiempo pensando.
    if len(moves) == 1:
        return moves[0]
        
    for move in moves:
        future_grid = apply_move(grid, move)
        # Evaluamos ese futuro (pasando el turno al humano)
        eval = minimax(future_grid, depth - 1, False)
        
        if eval > max_eval:
            max_eval = eval
            best_move = move
            
    return best_move