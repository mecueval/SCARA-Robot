# test/test_robot.py
import sys
import os

# Añadir ruta raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from hardware.robot_arm import RobotArm

def test_full_system():
    print("--- INICIANDO PRUEBA DE INTEGRACIÓN ---")
    
    # Instanciamos el brazo robot (lee los pines y medidas de config.py)
    brazo = RobotArm(config)
    
    # Queremos mover la ficha 50mm (5cm) en el eje X (hacia adelante)
    target_X = brazo.current_Px + 50.0
    target_Y = brazo.current_Py
    target_Z = brazo.current_Pz
    
    # Llamamos al comando principal
    brazo.move_linear(target_X, target_Y, target_Z, steps=20)
    
if __name__ == "__main__":
    test_full_system()