#!/usr/bin/env python3

'''
Punto de entrada al programa.

Maneja la toma de argumentos desde la terminal y ejecuta el programa. Ver ayuda
ejecutando este script con la opción --help
'''

import argparse
from dataclasses import dataclass

import parallax
import face_detection
import scene_3d
import scene_2d
from misc import RequestRestartException

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='comandos', dest='comando')
subparsers.required = True

# Lectura de argumentos

parser.add_argument('-s', '--screen-size', type=int, nargs=2,
    metavar=('WIDTH', 'HEIGHT'),
    help=('Seleccionar resolución pantalla a usar, ingresar ancho y alto en '
          'píxeles')
)

# Lectura de comando

parser_parallax = subparsers.add_parser(
    'parallax',
    help='Iniciar el programa completo'
)
parser_face_detection = subparsers.add_parser(
    'face_detection',
    help='Probar la detección de caras'
)
parser_scene_3d = subparsers.add_parser(
    'scene_3d',
    help='Probar escena 3d con OpenGL'
)
parser_scene_2d = subparsers.add_parser(
    'scene_2d',
    help='Probar escena 2d con OpenGL'
)

args = parser.parse_args()

# Al importar config se inicializa el objeto prm que almacena los parámetros o
# opciones
from config import prm

# Configurar argumentos

if args.screen_size:
    prm['screen_auto_size'] = False
    prm['screen_w'], prm['screen_h'] = args.screen_size
else:
    prm['screen_auto_size'] = True

# Ejecutar subprogramas dando los parámetros, parámetros por defecto y
# argumentos de terminal

while True:

    try:

        if args.comando == 'parallax':
            parallax.main()
        elif args.comando == 'face_detection':
            face_detection.demo()
        elif args.comando == 'scene_3d':
            scene_3d.demo()
        elif args.comando == 'scene_2d':
            scene_2d.demo()
        else:
            raise RuntimeError('Comando desconocido')

        # Si se llega acá significa que el programa terminó sin que se haya
        # pedido un reinicio
        break

    except RequestRestartException:
        print("Restarting (leaving parameters untouched)")
