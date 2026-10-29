# test/test_showcase.py
import sys
import os
import math
import numpy as np

# Añadir ruta raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from hardware.robot_arm import RobotArm

def print_jacobian_analysis(brazo, x, y, z):
    """
    Imprime el determinante Jacobiano para demostrar 
    que el robot no está en una posición inestable.
    """
    q1, q2, q3 = brazo.kinematics.inverse_kinematics(x, y, z)
    is_singular, det = brazo.kinematics.get_singularities(q2)
    
    print(f"  -> Determinante Jacobiano (Det): {det:.2f}")
    if is_singular:
        print("  -> ADVERTENCIA: ¡El robot está en una singularidad matemática! (Pérdida de un grado de libertad)")
    else:
        print("  -> Análisis de Singularidad: Superado. Cinemáticamente estable.")

def main():
    print("   DEMOSTRACIÓN ACADÉMICA: CINEMÁTICA Y CONTROL SCARA")

    # 1. Inicialización
    print("\n[FASE 1] INICIALIZANDO HARDWARE Y CINEMÁTICA...")
    brazo = RobotArm(config)
    
    # 2. Análisis del estado inicial
    print(f"\n[FASE 2] ESTADO INICIAL (HOME)")
    print(f"  -> Coordenadas cartesianas: X={brazo.current_Px} mm, Y={brazo.current_Py} mm")
    print_jacobian_analysis(brazo, brazo.current_Px, brazo.current_Py, brazo.current_Pz)

    # 3. Definición de objetivo
    objetivo_X = 180.0
    objetivo_Y = 50.0
    print(f"\n[FASE 3] PLANIFICACIÓN DE TRAYECTORIA LINEAL")
    print(f"  -> Objetivo cartesiano: X={objetivo_X} mm, Y={objetivo_Y} mm")
    print_jacobian_analysis(brazo, objetivo_X, objetivo_Y, brazo.current_Pz)

    # 4. Ejecución con telemetría en vivo
    print("\n[FASE 4] EJECUCIÓN FÍSICA (Interpolación en Tiempo Real)")
    # Le pasamos verbose=True para que imprima nuestra tabla mientras se mueve
    brazo.move_linear(objetivo_X, objetivo_Y, brazo.current_Pz, steps=15, verbose=True)

    print("[FASE 5] SECUENCIA TERMINADA CON ÉXITO.")

if __name__ == "__main__":
    main()