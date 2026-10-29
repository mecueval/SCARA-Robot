# hardware/robot_arm.py
import time
import math
from hardware.stepper import StepperMotor
from kinematics.scara import ScaraKinematics
from kinematics.trajectory import generate_linear_trajectory

class RobotArm:
    def __init__(self, config):
        """
        Controlador central del brazo SCARA. Integra cinemática y motores.
        """
        self.config = config
        
        # 1. Inicializar la Cinemática
        self.kinematics = ScaraKinematics(config.L1, config.L2, config.L3)
        
        # 2. Inicializar Motores (Hombro = q1, Codo = q2)
        self.motor_q1 = StepperMotor(
            step_pin=config.PIN_STEP_1, dir_pin=config.PIN_DIR_1,
            steps_per_rev=config.STEPS_PER_REV, microstepping=config.MICROSTEPPING, 
            gear_ratio=config.GEAR_RATIO
        )
        self.motor_q2 = StepperMotor(
            step_pin=config.PIN_STEP_2, dir_pin=config.PIN_DIR_2,
            steps_per_rev=config.STEPS_PER_REV, microstepping=config.MICROSTEPPING, 
            gear_ratio=config.GEAR_RATIO
        )
        
        # 3. Estado interno cartesiano
        # Asumimos que el robot arranca en una posición "Home" conocida.
        self.current_Px = 100.0
        self.current_Py = 0.0
        self.current_Pz = 20.0
        
        # Sincronizamos los motores con esta posición inicial
        q1, q2, q3 = self.kinematics.inverse_kinematics(
            self.current_Px, self.current_Py, self.current_Pz
        )
        self.motor_q1.set_current_angle(q1)
        self.motor_q2.set_current_angle(q2)
        
        print(f"Brazo inicializado en Home: ({self.current_Px}, {self.current_Py})")

    def _sync_move(self, steps1, dir1, steps2, dir2, delay=0.001):
        """
        Ejecuta pasos en ambos motores de forma simultánea e interpolada.
        Garantiza que ambos motores terminen su recorrido al mismo tiempo.
        """
        # Configurar pines de dirección
        self.motor_q1.dir_pin.value = 1 if dir1 else 0
        self.motor_q2.dir_pin.value = 1 if dir2 else 0

        # El motor que tiene que dar más pasos dicta la duración del bucle
        max_steps = max(steps1, steps2)
        if max_steps == 0:
            return

        # Ratios de avance por cada iteración del bucle (Algoritmo DDA)
        ratio1 = steps1 / max_steps
        ratio2 = steps2 / max_steps

        counter1 = 0.0
        counter2 = 0.0

        # Bucle maestro de generación de pulsos
        for _ in range(max_steps):
            counter1 += ratio1
            counter2 += ratio2

            # Acumulador: Si supera 1.0, toca dar un paso en este motor
            step_q1_now = False
            step_q2_now = False

            if counter1 >= 1.0:
                self.motor_q1.step_pin.on()
                counter1 -= 1.0
                step_q1_now = True
                
            if counter2 >= 1.0:
                self.motor_q2.step_pin.on()
                counter2 -= 1.0
                step_q2_now = True

            time.sleep(delay) # Mantener pulso en ALTO

            # Apagar los pines que se hayan encendido (Flanco de bajada)
            if step_q1_now: self.motor_q1.step_pin.off()
            if step_q2_now: self.motor_q2.step_pin.off()
            
            time.sleep(delay) # Tiempo mínimo en BAJO antes del siguiente pulso

    def move_linear(self, end_Px, end_Py, end_Pz, steps=30, verbose=True):
        """
        Mueve el brazo en línea recta. Si verbose=True, imprime telemetría en tiempo real.
        """
        if verbose:
            print("\n" + "="*85)
            print(f"{'WP':<3} | {'X (mm)':<7} | {'Y (mm)':<7} | {'q1 (°)':<7} | {'q2 (°)':<7} | {'Pulsos M1':<11} | {'Pulsos M2':<11} | {'Estado'}")
            print("-" * 85)

        start_point = (self.current_Px, self.current_Py, self.current_Pz)
        end_point = (end_Px, end_Py, end_Pz)
        
        waypoints = generate_linear_trajectory(start_point, end_point, steps)
        
        for i, (px, py, pz) in enumerate(waypoints):
            try:
                # 1. Cinemática Inversa (Matemática Pura)
                q1, q2, q3 = self.kinematics.inverse_kinematics(px, py, pz, elbow_right=True)
                
                # 2. Conversión a hardware (Discretización a pasos)
                steps1, dir1 = self.motor_q1.rad_to_steps(q1)
                steps2, dir2 = self.motor_q2.rad_to_steps(q2)
                
                # Telemetría para el profesor
                if verbose:
                    m1_sign = "+" if dir1 else "-"
                    m2_sign = "+" if dir2 else "-"
                    print(f"{i:<3} | {px:<7.1f} | {py:<7.1f} | {math.degrees(q1):<7.1f} | {math.degrees(q2):<7.1f} | {m1_sign}{steps1:<10} | {m2_sign}{steps2:<10} | OK")
                
                # 3. Ejecución física (Algoritmo DDA)
                self._sync_move(steps1, dir1, steps2, dir2, delay=0.001)
                
                # 4. Actualizar memoria interna
                self.motor_q1.set_current_angle(q1)
                self.motor_q2.set_current_angle(q2)
                
            except ValueError as e:
                if verbose:
                    print(f"{i:<3} | {px:<7.1f} | {py:<7.1f} | {'ERROR':<7} | {'ERROR':<7} | {'-':<11} | {'-':<11} | SINGULARIDAD!")
                break
                
        self.current_Px = end_Px
        self.current_Py = end_Py
        self.current_Pz = end_Pz
        if verbose:
            print("="*85 + "\n")