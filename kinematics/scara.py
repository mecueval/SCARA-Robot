# kinematics/scara.py
import numpy as np
import math

class ScaraKinematics:
    def __init__(self, L1, L2, L3):
        """
        Inicializa la cinemática según la notación de tu modelo en MATLAB.
        L1: Altura base del robot (eje Z).
        L2: Longitud del primer brazo horizontal (hombro a codo).
        L3: Longitud del segundo brazo horizontal (codo a punta).
        """
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3

    def forward_kinematics(self, q1, q2, q3):
        """
        Cinemática Directa: Calcula (Px, Py, Pz) a partir de (q1, q2, q3).
        q1, q2: Ángulos en radianes.
        q3: Desplazamiento lineal del eje Z.
        Retorna: Tupla (Px, Py, Pz).
        """
        Px = self.L2 * math.cos(q1) + self.L3 * math.cos(q1 + q2)
        Py = self.L2 * math.sin(q1) + self.L3 * math.sin(q1 + q2)
        Pz = self.L1 - q3
        
        return Px, Py, Pz

    def inverse_kinematics(self, Px, Py, Pz, elbow_right=True):
        """
        Cinemática Inversa: Calcula (q1, q2, q3) usando tu Método Geométrico.
        Px, Py, Pz: Coordenadas objetivo espaciales.
        elbow_right: Define si tomamos la raíz positiva o negativa para sen(q2).
        Retorna: Tupla (q1, q2, q3).
        """
        # 1. Articulación prismática (Eje Z)
        q3 = self.L1 - Pz
        
        # 2. Articulación del codo (q2)
        cos_q2 = (Py**2 + Px**2 - self.L2**2 - self.L3**2) / (2 * self.L2 * self.L3)
        
        # Proteger contra errores de punto flotante fuera de dominio [-1, 1]
        cos_q2 = max(-1.0, min(1.0, cos_q2))
        
        # Calculamos sen(q2) tomando la raíz
        sen_q2_val = math.sqrt(1 - cos_q2**2)
        
        # La solución de "codo a la derecha" o "codo a la izquierda"
        # depende del signo que le asignemos al seno
        sen_q2 = sen_q2_val if elbow_right else -sen_q2_val
        
        q2 = math.atan2(sen_q2, cos_q2)

        # 3. Articulación del hombro (q1) usando el Método Geométrico
        termino1_geom = math.atan2(Py, Px)
        termino2_geom = math.atan2((self.L3 * sen_q2), (self.L2 + self.L3 * cos_q2))
        
        q1 = termino1_geom - termino2_geom

        return q1, q2, q3

    def get_jacobian(self, q1, q2):
        """
        Matriz Jacobiana Analítica (3x3).
        Relaciona las velocidades articulares [dq1, dq2, dq3] con [dPx, dPy, dPz].
        El eje Z es completamente independiente de (q1, q2), por lo que las
        derivadas cruzadas son cero y dPz/dq3 = -1 (basado en Pz = L1 - q3).
        """
        # Fila 1: dx/dq1, dx/dq2, dx/dq3
        j11 = -self.L2 * math.sin(q1) - self.L3 * math.sin(q1 + q2)
        j12 = -self.L3 * math.sin(q1 + q2)
        j13 = 0.0
        
        # Fila 2: dy/dq1, dy/dq2, dy/dq3
        j21 = self.L2 * math.cos(q1) + self.L3 * math.cos(q1 + q2)
        j22 = self.L3 * math.cos(q1 + q2)
        j23 = 0.0
        
        # Fila 3: dz/dq1, dz/dq2, dz/dq3
        j31 = 0.0
        j32 = 0.0
        j33 = -1.0  # Derivada de (L1 - q3) respecto a q3

        return np.array([
            [j11, j12, j13],
            [j21, j22, j23],
            [j31, j32, j33]
        ])

    def get_singularities(self, q2):
        """
        Calcula el determinante del Jacobiano 3x3.
        """
        # El determinante de esta matriz 3x3 se reduce a -1 * det(J_2x2)
        determinant = -1 * (self.L2 * self.L3 * math.sin(q2))
        
        is_singular = abs(determinant) < 1e-3
        return is_singular, determinant

    def get_inverse_jacobian(self, q1, q2):
        """
        Matriz Jacobiana Inversa (3x3).
        Permite calcular las velocidades articulares [dq1, dq2, dq3]
        necesarias para alcanzar una velocidad cartesiana [dPx, dPy, dPz].
        """
        # 1. Obtenemos el determinante del bloque 2x2 (q1, q2)
        # det(J) = -L2 * L3 * sin(q2)
        is_singular, det_3x3 = self.get_singularities(q2)

         # Validación de singularidad 
        if is_singular:
            raise ValueError("El robot esta en una singularidad.")
       
        det = -det_3x3
        # 2. Términos trigonométricos
        sin_q1 = math.sin(q1)
        cos_q1 = math.cos(q1)
        sin_q12 = math.sin(q1 + q2)
        cos_q12 = math.cos(q1 + q2)

        # 3. Elementos de la Jacobiana Inversa Analítica 2x2
        # J_inv = (1/det) * [ J22  -J12 ]
        #                   [-J21   J11 ]
        
        j_inv_11 = (self.L3 * cos_q12) / det
        j_inv_12 = (self.L3 * sin_q12) / det
        j_inv_13 = 0.0
        
        j_inv_21 = -(self.L2 * cos_q1 + self.L3 * cos_q12) / det
        j_inv_22 = -(self.L2 * sin_q1 + self.L3 * sin_q12) / det
        j_inv_23 = 0.0
        
        # 4. Fila 3 (Eje Z). Pz = L1 - q3  --> dPz/dq3 = -1 --> dq3/dPz = -1
        j_inv_31 = 0.0
        j_inv_32 = 0.0
        j_inv_33 = -1.0

        return np.array([
            [j_inv_11, j_inv_12, j_inv_13],
            [j_inv_21, j_inv_22, j_inv_23],
            [j_inv_31, j_inv_32, j_inv_33]
        ])