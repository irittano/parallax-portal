'''
Cosas varias
'''

import numpy as np

from config import prm

class RequestRestartException(Exception):
    '''
    No es realmente una excepción sino que provoca que el programa se reinicie

    Lo uso para que al cambiar ciertos parámetros uno pueda reiniciar el
    programa haciendo "raise RequestRestartException()", pero al mismo tiempo
    mantener los parámetros cambiados.

    Funciona porque main.py se encarga de reiniciar cuando esta excepción
    ocurre.
    '''

class PositionFilter:

    def __init__(self):
        '''
        Filtro para la detección de cabeza

        Suaviza las coordenadas X, Y, Z de la posición de la cabeza en
        centimetros

        Basado en https://www.cs.utexas.edu/~teammco/misc/kalman_filter/

        Otra explicación:
        https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/

        Variables en minúscula son vectores, en mayúscula son matrices

        No tenemos vector de control que se le suele llamar c, por lo tanto
        tampoco usamos matriz B
        '''

        # Matriz de estimación de error, se puede dejar en cero y luego se va
        # actualizando en cada paso
        self.P = np.array([
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
        ])

        # Se puede usar para determinar qué estados se pueden medir y cuales no
        #  h = 0.1
        h = prm['filter_h']
        self.H = np.array([
            [ 1, 0, 0, h, 0, 0],
            [ 0, 1, 0, 0, h, 0],
            [ 0, 0, 1, 0, 0, h],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
        ])

        # Error de acción, mientras mayor es el valor significa que se confía
        # menos en las predicciones de las ecuaciones y más en los datos reales
        #  q = 0.1
        q = prm['filter_q']
        self.Q = np.array([
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, q, 0, 0],
            [ 0, 0, 0, 0, q, 0],
            [ 0, 0, 0, 0, 0, q],
        ])

        # Error de sensor, mientras mayor es el valor significa que se confía
        # menos en las mediciones reales
        #  r = 0.2
        r = prm['filter_r']
        self.R = np.array([
            [ r, 0, 0, 0, 0, 0],
            [ 0, r, 0, 0, 0, 0],
            [ 0, 0, r, 0, 0, 0],
            [ 0, 0, 0, r, 0, 0],
            [ 0, 0, 0, 0, r, 0],
            [ 0, 0, 0, 0, 0, r],
        ])

        # Estimación de estado, se va actualizando
        self.x = np.array([0, 0, 0, 0, 0, 0])

        # Matriz identidad, la defino por conveniencia
        self.I = np.identity(6)

        # Temporizador de salto, cuenta el tiempo desde el último salto detectado
        self.jump_timer = 0

    def filter(self, delta_t, pos):
        '''
        Ejecutar un paso del filtro

        Ingresar tiempo en segundos desde último filtrado y nuevo vector de
        posicion: [X, Y, Z]
        '''

        # Incrementar timer de salto con el tiempo pasado desde ultimo frame
        self.jump_timer += delta_t

        # Si el filtro está deshabilitado, almacenar posición (dejando
        # velocidades en cero) y devolver lo mismo que se recibió
        if not prm['filter_enabled']:
            self.x = np.append(pos, (0, 0, 0))
            return pos

        # Matrix de predicción, se usa para decir que en la predicción
        # nuevo_x = A * viejo_x
        # Las tres primeras filas dicen que la nueva posición es igual a la
        # anterior más delta_t por velocidad
        # Las otras tres dicen que la nueva velocidad es igual a la anterior
        # menos una fricción por delta_t
        dt = delta_t
        a = prm['filter_a']
        self.A = np.array([
            [  1,  0,  0, dt,  0,  0],
            [  0,  1,  0,  0, dt,  0],
            [  0,  0,  1,  0,  0, dt],
            [  0,  0,  0,  a,  0,  0],
            [  0,  0,  0,  0,  a,  0],
            [  0,  0,  0,  0,  0,  a],
        ])

        # Calcular velocidades y crear vector de medición
        m = np.append(pos, self.x[3:])

        # Paso de predicción

        self.x = (self.A @ self.x)
        self.P = (self.A @ self.P @ self.A.T) + self.Q

        # Paso de corrección

        S = (self.H @ self.P @ self.H.T) + self.R
        K = (self.P @ self.H.T) @ np.linalg.inv(S)
        y = m - (self.H @ self.x)

        self.x = self.x + (K @ y)
        self.P = (self.I - (K @ self.H)) @ self.P

        jump_detected = False
        if self.x[4] < -prm['filter_v_threshold']:
            # Salto detectado debido a velocidad vertical
            if self.jump_timer > prm['filter_jump_timer']:
                # Pasó suficiente tiempo desde último salto
                jump_detected = True
                self.jump_timer = 0

        return self.x[:3], jump_detected

    def predict(self, delta_t):

        # Si el filtro está deshabilitado devolver última posición
        if not prm['filter_enabled']:
            return self.x[:3]

        # Incrementar timer de salto con el tiempo pasado desde ultimo frame
        self.jump_timer += delta_t

        # Matrix de predicción, se usa para decir que en la predicción
        # nuevo_x = A * viejo_x
        # Las tres primeras filas dicen que la nueva posición es igual a la
        # anterior más delta_t por velocidad
        # Las otras tres dicen que la nueva velocidad es igual a la anterior
        # menos una fricción por delta_t
        dt = delta_t
        a = prm['filter_a']
        self.A = np.array([
            [  1,  0,  0, dt,  0,  0],
            [  0,  1,  0,  0, dt,  0],
            [  0,  0,  1,  0,  0, dt],
            [  0,  0,  0,  a,  0,  0],
            [  0,  0,  0,  0,  a,  0],
            [  0,  0,  0,  0,  0,  a],
        ])

        # Paso de predicción

        self.x = (self.A @ self.x)
        self.P = (self.A @ self.P @ self.A.T) + self.Q

        return self.x[:3]
