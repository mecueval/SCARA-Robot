import sys
import os
import math
import matplotlib.pyplot as plt

# Añadir el directorio raíz del proyecto a las rutas de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from kinematics.scara import ScaraKinematics
from kinematics.trajectory import generate_linear_trajectory

def test_straight_line():
    robot = ScaraKinematics(config.L1, config.L2, config.L3)

    # 1. Definir dos casillas en el tablero (Inicio y Fin)
    # Ej: Desde el centro bajo del tablero hasta una esquina superior
    start_point = (100.0, -40.0, 20.0)  
    end_point = (180.0, 60.0, 20.0)     

    print("Generando trayectoria...")
    # Generamos 20 pasos (21 puntos en total)
    waypoints = generate_linear_trajectory(start_point, end_point, steps=20)

    # Listas para guardar los datos y graficarlos luego
    x_vals, y_vals = [], []
    q1_vals, q2_vals = [], []

    print(f"{'Paso':<5} | {'Px':<7} | {'Py':<7} | {'q1 (grados)':<12} | {'q2 (grados)':<12}")
    print("-" * 55)

    # 2. Iterar por cada punto de la trayectoria
    for i, (px, py, pz) in enumerate(waypoints):
        try:
            # Calcular la cinemática inversa para este punto exacto
            q1, q2, q3 = robot.inverse_kinematics(px, py, pz, elbow_right=True)
            
            # Guardar para la gráfica
            x_vals.append(px)
            y_vals.append(py)
            q1_vals.append(math.degrees(q1))
            q2_vals.append(math.degrees(q2))
            
            # Imprimir los primeros y últimos para no saturar la consola
            if i < 3 or i > 17:
                print(f"{i:<5} | {px:<7.1f} | {py:<7.1f} | {math.degrees(q1):<12.2f} | {math.degrees(q2):<12.2f}")
            elif i == 3:
                print(f"...   | ...     | ...     | ...          | ...")

        except ValueError as e:
            print(f"Error en paso {i} (X:{px}, Y:{py}): {e}")
            return

    # 3. Graficar los resultados
    print("\nTrayectoria calculada con éxito. Abriendo gráfica...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfica Cartesiana (Lo que hace el efector final)
    ax1.plot(x_vals, y_vals, marker='o', color='blue', linestyle='-')
    ax1.plot(start_point[0], start_point[1], marker='s', color='green', markersize=10, label="Inicio")
    ax1.plot(end_point[0], end_point[1], marker='X', color='red', markersize=10, label="Fin")
    ax1.set_title("Espacio Cartesiano (X, Y)\n¡Debe ser una línea recta perfecta!")
    ax1.set_xlabel("Eje X (mm)")
    ax1.set_ylabel("Eje Y (mm)")
    ax1.grid(True)
    ax1.legend()
    ax1.axis('equal') # Mantener proporción 1:1

    # Gráfica Articular (Lo que hacen los motores)
    ax2.plot(range(len(q1_vals)), q1_vals, marker='.', color='orange', label='q1 (Hombro)')
    ax2.plot(range(len(q2_vals)), q2_vals, marker='.', color='purple', label='q2 (Codo)')
    ax2.set_title("Espacio Articular (q1, q2)\nCurvas no lineales suaves")
    ax2.set_xlabel("Waypoints (Paso)")
    ax2.set_ylabel("Ángulo (grados)")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_straight_line()