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

        Otra explicación:
        https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/

        Variables en minúscula son vectores, en mayúscula son matrices

        No tenemos vector de control que se le suele llamar c, por lo tanto
        tampoco usamos matriz B

        TODO: Sacar?
        Es importante dar los FPS esperados ya que se usará para calcular
        velocidades y ese tipo de cosas. Es necesario especificarlo porque se
        utiliza ese valor para las predicciones.
        '''

        self.H = np.array([
            [   1,   0,   0,   0.1,   0,   0],
            [   0,   1,   0,   0,   0.1,   0],
            [   0,   0,   1,   0,   0,   0.1],
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

        self.x = np.array([0, 0, 0, 0, 0, 0])

    def filter(self, delta_t, pos):
        '''
        Ejecutar un paso del filtro

        Ingresar tiempo en segundos desde último filtrado y nuevo vector de
        posicion: [X, Y, Z]
        '''

        # Matrix de predicción, se usa para decir que en la predicción
        # nuevo_x = A * viejo_x
        # Las tres primeras filas dicen que la nueva posición es igual a la
        # anterior más delta_t por velocidad
        # Las otras tres dicen que la nueva velocidad es igual a la anterior
        # menos una fricción por delta_t
        dt = delta_t
        self.A = np.array([
            [  1,  0,  0, dt,  0,  0],
            [  0,  1,  0,  0, dt,  0],
            [  0,  0,  1,  0,  0, dt],
            [  0,  0,  0,  1,  0,  0],
            [  0,  0,  0,  0,  1,  0],
            [  0,  0,  0,  0,  0,  1],
        ])

        # Calcular velocidades y crear vector de medición
        vel = (pos - self.x[:3]) / delta_t
        m = np.append(pos, self.x[3:])

        # Paso de predicción

        x = (self.A @ self.x)
        P = (self.A @ self.P @ self.A.T) + self.Q

        # Paso de corrección

        S = (self.H @ self.P @ self.H.T) + self.R
        K = (self.P @ self.H.T) @ np.linalg.inv(S)
        y = m - (self.H @ self.x)

        cur_x = x + (K @ y)
        cur_P = (self.I - (K @ self.H)) @ P

        self.x = cur_x
        self.P = cur_P

        print(self.x)

        #  pred_x = self.x
        #  for i in range(10):
            #  pred_x = (self.A @ pred_x)

        #  return pred_x[:3]
        return self.x[:3]
