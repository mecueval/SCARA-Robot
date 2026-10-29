import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.stepper import StepperMotor

# Simular el motor del hombro (con datos falsos de pines)
motor_hombro = StepperMotor(step_pin=21, dir_pin=20, steps_per_rev=200, microstepping=16, gear_ratio=3.0)

# ¿Cuántos pasos son 45 grados (pi/4)?
pasos, direccion = motor_hombro.rad_to_steps(math.pi / 4)
print(f"Para mover 45°: Se requieren {pasos} pasos. Hacia adelante: {direccion}")