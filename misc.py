'''
Cosas varias
'''

class RequestRestartException(Exception):
    '''
    No es realmente una excepción sino que provoca que el programa se reinicie

    Lo uso para que al cambiar ciertos parámetros uno pueda reiniciar el
    programa haciendo "raise RequestRestartException()", pero al mismo tiempo
    mantener los parámetros cambiados.

    Funciona porque main.py se encarga de reiniciar cuando esta excepción
    ocurre.
    '''
