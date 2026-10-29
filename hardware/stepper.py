# hardware/stepper.py
import time
import math
from gpiozero import OutputDevice

class StepperMotor:
    def __init__(self, step_pin, dir_pin, steps_per_rev, microstepping, gear_ratio):
        """
        Inicializa un motor paso a paso controlado por un driver A4988.
        """
        # OutputDevice es la forma más limpia y compatible de controlar pines en Pi 5
        self.step_pin = OutputDevice(step_pin)
        self.dir_pin = OutputDevice(dir_pin)
        
        # Matemáticas de resolución
        self.steps_per_rev = steps_per_rev
        self.microstepping = microstepping
        self.gear_ratio = gear_ratio
        
        # ¿Cuántos pasos se necesitan para que el BRAZO dé un giro completo (360°)?
        self.total_steps_360 = self.steps_per_rev * self.microstepping * self.gear_ratio
        
        # Rastrear la posición actual en radianes
        self.current_angle = 0.0  

    def rad_to_steps(self, target_angle_rad):
        """
        Calcula cuántos pasos debe dar el motor para alcanzar el nuevo ángulo.
        Retorna la cantidad de pasos (int) y la dirección (bool).
        """
        delta_angle = target_angle_rad - self.current_angle
        delta_degrees = math.degrees(delta_angle)
        
        # Regla de tres simple: (grados_a_mover / 360) * pasos_totales
        steps_float = (abs(delta_degrees) / 360.0) * self.total_steps_360
        steps = int(round(steps_float))
        
        # Dirección: True si es positivo (horario), False si es negativo (antihorario)
        direction = delta_angle >= 0
        
        return steps, direction

    def move_steps(self, steps, direction, delay=0.001):
        """
        Envía los pulsos físicos al driver A4988.
        """
        if steps == 0:
            return
            
        # 1. Configurar la dirección (HIGH o LOW)
        self.dir_pin.value = 1 if direction else 0
        
        # 2. Bucle de pulsos (Generar la onda cuadrada)
        for _ in range(steps):
            self.step_pin.on()
            time.sleep(delay)  # Tiempo en HIGH (1 milisegundo por defecto)
            self.step_pin.off()
            time.sleep(delay)  # Tiempo en LOW

    def set_current_angle(self, current_angle_rad):
        """
        Actualiza el ángulo interno después de un movimiento.
        """
        self.current_angle = current_angle_rad