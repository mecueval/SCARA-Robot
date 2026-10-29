# tests/test_kinematics.py
import sys
import os
import math
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from kinematics.scara import ScaraKinematics

def run_tests():
    # 1. Inicializar el robot con las constantes de tu config
    # Nota: Asegúrate de tener L1, L2, L3 definidos en config.py
    robot = ScaraKinematics(config.L1, config.L2, config.L3)

    # 2. Definir un punto objetivo dentro del tablero
    target_Px = 150.0
    target_Py = 10.0
    target_Pz = 5.0  # Altura de la ficha

    print(f"--- 1. OBJETIVO CARTESIANO ---")
    print(f"Px: {target_Px}, Py: {target_Py}, Pz: {target_Pz}\n")

    # 3. Probar Cinemática Inversa (IK)
    q1, q2, q3 = robot.inverse_kinematics(target_Px, target_Py, target_Pz, elbow_right=True)
    
    print(f"--- 2. CINEMÁTICA INVERSA (Ángulos calculados) ---")
    print(f"q1: {math.degrees(q1):.2f}° ({q1:.4f} rad)")
    print(f"q2: {math.degrees(q2):.2f}° ({q2:.4f} rad)")
    print(f"q3: {q3:.2f} mm (Desplazamiento Z)\n")

    # 4. Probar Cinemática Directa (FK) usando los resultados de la IK
    calc_Px, calc_Py, calc_Pz = robot.forward_kinematics(q1, q2, q3)
    
    print(f"--- 3. CINEMÁTICA DIRECTA (Validación) ---")
    print(f"Px calculado: {calc_Px:.4f} (Error: {abs(target_Px - calc_Px):.4e})")
    print(f"Py calculado: {calc_Py:.4f} (Error: {abs(target_Py - calc_Py):.4e})")
    print(f"Pz calculado: {calc_Pz:.4f} (Error: {abs(target_Pz - calc_Pz):.4e})\n")

    # 5. Probar Matrices Jacobianas
    print(f"--- 4. ANÁLISIS JACOBIANO ---")
    J = robot.get_jacobian(q1, q2)
    J_inv = robot.get_inverse_jacobian(q1, q2)
    
    print("Matriz Jacobiana Directa (J):")
    print(np.round(J, 4))
    
    print("\nMatriz Jacobiana Inversa (J_inv):")
    print(np.round(J_inv, 4))

    # Prueba de fuego algebraica: J * J_inv debe ser la Matriz Identidad
    identidad_calculada = np.round(np.dot(J, J_inv), 4) + 0.0
    print("\nPrueba de Identidad (J * J_inv):")
    print(np.round(identidad_calculada, 4))

if __name__ == "__main__":
    run_tests()