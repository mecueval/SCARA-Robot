import math

def generate_linear_trajectory(start_P, end_P, steps=50):
    """
    Genera puntos intermedios en línea recta cartesiana.
    start_P, end_P: Tuplas (Px, Py, Pz) de inicio y fin.
    steps: Cantidad de subdivisiones (resolución de la recta).
    Retorna: Lista de tuplas (Px, Py, Pz)
    """
    trajectory = []
    
    for i in range(steps + 1):
        t = i / steps
        # Interpolación lineal simple paramétrica para X, Y y Z
        x = start_P[0] + (end_P[0] - start_P[0]) * t
        y = start_P[1] + (end_P[1] - start_P[1]) * t
        z = start_P[2] + (end_P[2] - start_P[2]) * t
        
        trajectory.append((x, y, z))
        
    return trajectory