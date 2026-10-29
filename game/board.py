# game/board.py

class SimpleCheckers:
    def __init__(self, config):
        self.config = config
        self.rows = config.BOARD_ROWS
        self.cols = config.BOARD_COLS
        self.square_size = config.SQUARE_SIZE
        
        # Estado del tablero: 0 (Vacío), 1 (Fichas Humano), 2 (Fichas Robot)
        self.grid = self._initialize_grid()

    def _initialize_grid(self):
        """
        Crea la matriz 8x8. 
        El robot (2) empieza en las filas 0 y 1 (más cerca de su base).
        El humano (1) empieza en las filas 6 y 7 (más lejos).
        """
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Las fichas solo van en las casillas oscuras (row + col impar)
                if (row + col) % 2 != 0:
                    if row < 2:          # Dos filas para el robot
                        grid[row][col] = 2
                    elif row > 5:        # Dos filas para el humano
                        grid[row][col] = 1
        return grid

    def get_physical_coordinates(self, row, col):
        """
        Traduce una posición lógica [fila][columna] a milímetros (X, Y).
        - Fila 0 es la más cercana a la base del robot (Eje X mínimo).
        - Columna 0 es la más a la derecha (Eje Y negativo).
        """
        # Calcular X (Profundidad)
        # Offset inicial + casillas anteriores + mitad de la casilla actual (para apuntar al centro)
        px = self.config.BOARD_OFFSET_X + (row * self.square_size) + (self.square_size / 2.0)
        
        # Calcular Y (Ancho - Izquierda/Derecha)
        # Calculamos el ancho total para centrar el tablero en Y = 0
        board_width = self.cols * self.square_size
        py = (col * self.square_size) + (self.square_size / 2.0) - (board_width / 2.0)
        
        return px, py

    def print_board(self):
        """
        Imprime el estado visual del tablero en consola.
        """
        print("\n  Tablero de Damas (Visión Lógica)")
        print("    " + "   ".join([str(c) for c in range(self.cols)]))
        print("  +" + "---+" * self.cols)
        for r in range(self.rows):
            row_str = f"{r} |"
            for c in range(self.cols):
                val = self.grid[r][c]
                char = " "
                if val == 1: char = "H" # Humano
                if val == 2: char = "R" # Robot
                row_str += f" {char} |"
            print(row_str)
            print("  +" + "---+" * self.cols)
        print()