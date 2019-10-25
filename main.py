#!/usr/bin/env python3

'''
Punto de entrada al programa.

Maneja la toma de argumentos desde la terminal y tiene todas las variables por
defecto. Ver ayuda ejecutando este script con la opción --help
'''

import argparse
from dataclasses import dataclass

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='comandos', dest='comando')
subparsers.required = True

# Objeto que mantiene todos los parametros configurables del programa, permite
# tener todo en un solo lugar para luego cambiarlos durante la ejecucion del
# programa

@dataclass
class Parameters:
    face_detection_minsize = 30
    face_detection_min_neighbors = 15
    face_detection_scale_factor = 1.2

prm = Parameters()

# Parametros por defecto, los mantenemos acá para tener como referencia y saber
# cuales cambiamos. Este objeto no deberia ser modificado nunca
default_prm = Parameters()

# Lectura de argumentos

parser_facecascade = subparsers.add_parser(
    'face_detection',
    help='Probar la detección de caras'
)
parser_opengl = subparsers.add_parser(
    'scene_3d',
    help='Probar escena 3d con OpenGL'
)
parser_opengl = subparsers.add_parser(
    'scene_2d',
    help='Probar escena 2d con OpenGL'
)

args = parser.parse_args()

# Ejecutar subprogramas dando los parámetros, parámetros por defecto y
# argumentos de terminal

import face_detection
import scene_3d
import scene_2d

if args.comando == 'face_detection':
    face_detection.main(prm, default_prm, args)
elif args.comando == 'scene_3d':
    scene_3d.main(prm, default_prm, args)
elif args.comando == 'scene_2d':
    scene_2d.main(prm, default_prm, args)
else:
    RuntimeError('Comando desconocido')
