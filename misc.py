'''
Cosas varias
'''

import numpy as np

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

        Variables en minúscula son vectores, en mayúscula son matrices
        '''

        # Vector de ultima posición, usado para calcular velocidades
        self.last_pos = None

        self.A = np.array([
            [   1,   0,   0, 0.2,   0,   0],
            [   0,   1,   0,   0, 0.2,   0],
            [   0,   0,   1,   0,   0, 0.2],
            [   0,   0,   0,   1,   0,   0],
            [   0,   0,   0,   0,   1,   0],
            [   0,   0,   0,   0,   0,   1],
        ])

        self.B = np.array([
            [   1,   0,   0,   0,   0,   0],
            [   0,   1,   0,   0,   0,   0],
            [   0,   0,   1,   0,   0,   0],
            [   0,   0,   0,   1,   0,   0],
            [   0,   0,   0,   0,   1,   0],
            [   0,   0,   0,   0,   0,   1],
        ])

        self.H = np.array([
            [   1,   0,   0,   1,   0,   0],
            [   0,   1,   0,   0,   1,   0],
            [   0,   0,   1,   0,   0,   1],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
        ])

        self.Q = np.array([
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0, 0.1,   0,   0],
            [   0,   0,   0,   0, 0.1,   0],
            [   0,   0,   0,   0,   0, 0.1],
        ])

        self.R = np.array([
            [ 0.1,   0,   0,   0,   0,   0],
            [   0, 0.1,   0,   0,   0,   0],
            [   0,   0, 0.1,   0,   0,   0],
            [   0,   0,   0, 0.1,   0,   0],
            [   0,   0,   0,   0, 0.1,   0],
            [   0,   0,   0,   0,   0, 0.1],
        ])

        self.P = np.array([
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
            [   0,   0,   0,   0,   0,   0],
        ])

        self.I = np.identity(6)

        self.c = np.array([0, 0, 0, 0, 0, 0])
        self.x = np.array([0, 0, 0, 0, 0, 0])

    def filter(self, delta_t, pos):
        '''
        Ejecutar un paso del filtro

        Ingresar tiempo en segundos desde último filtrado y nuevo vector de
        posicion: [X, Y, Z]
        '''

        if self.last_pos is None:
            # No hacer nada, devolver el vector recibido y guardar la posición
            # para la próxima
            self.last_pos = pos
            return pos


        # Calcular velocidades y crear vector de medición
        velocity = (pos - self.last_pos) / delta_t
        m = np.append(pos, velocity)

        # Paso de predicción

        self.x = (self.A @ self.x) + (self.B @ self.c)
        self.P = (self.A @ self.P @ self.A.T) + self.Q

        # Paso de corrección

        S = (self.H @ self.P @ self.H.T) + self.R
        K = (self.P @ self.H.T) @ np.linalg.inv(S)
        y = m - (self.H @ self.x)
        self.x = self.x + (K @ y)
        P = (self.I - (K @ self.H)) @ self.P

        self.last_pos = pos


        return self.x[:3]
