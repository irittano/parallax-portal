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

# Lectura de argumentos

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

# Ejecutar subprogramas dando los parámetros, parámetros por defecto y
# argumentos de terminal

import parallax
import face_detection
import scene_3d
import scene_2d

if args.comando == 'parallax':
    parallax.main()
elif args.comando == 'face_detection':
    face_detection.demo()
elif args.comando == 'scene_3d':
    scene_3d.demo()
elif args.comando == 'scene_2d':
    scene_2d.demo()
else:
    RuntimeError('Comando desconocido')
