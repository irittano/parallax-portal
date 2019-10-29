'''
Funciones relacionadas a OpenGL para el dibujado de una escena 3D

Coordenadas:
- X positivo hacia la derecha
- Y positivo hacia arriba
- Z positivo hacia afuera de la pantalla (la persona está en Z positivo y los
  objetos en Z negativo)
- Distancias en centimetros
'''

import video

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
import numpy as np

MIN_Z = -60 # cm
NEAR_Z = 1 # cm
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (1, 1, 1)
COLOR_RED = (1, 0, 0)
COLOR_GREEN = (0, 1, 0)
COLOR_BLUE = (0, 0, 1)

def get_cam_from_mouse(window_s):
    '''
    Obtener coordenadas de la camara desde la posicion del mouse

    Dar como argumento tuple de ancho y alto de pantalla en pixeles

    Posicion Z de la camara fija en 30
    '''
    mouse = pygame.mouse.get_pos()
    pos = np.divide(
            np.subtract(
                np.divide(window_s, 2),
                mouse
            ),
            6
        )

    return (pos[0], -pos[1], 30)

def draw_line_to_inf(x, y, z):
    '''
    Dibujar linea desde posicion dada hasta un gran Z
    '''
    glBegin(GL_LINE_LOOP)

    glColor3f(*COLOR_WHITE)
    glVertex3f(x, y, z)
    glColor3f(*COLOR_BLACK)
    glVertex3f(x, y, MIN_Z)

    glEnd()

def draw_cube(x, y, z, size):
    '''
    Dibujar cubo

    Configurar color antes
    '''
    glTranslatef(x, y, z)
    glutSolidCube(size)
    glTranslatef(-x, -y, -z)

def set_camera(prm, cam, screen, window_s):
    '''
    Configura la camara en la posicion dada
    '''

    if prm.scene_3d_perspective:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, window_s[0] / window_s[1], 1, 250)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(cam[0], cam[1], cam[2], 0, 0, 0, 0, 1, 0)

    else:
        # SKEWED FRUSTRUM / OFF-AXIS PROJECTION
        # Basada en la implementación de
        # https://github.com/agirault/screenReality
        # basada en el paper:
        # Name:   Generalized Perspective Projection
        # Author: Robert Kooima
        # Date:   August 2008, revised June 2009

        # space corners coordinates
        pa = np.array((-screen[0], -screen[1], 0))
        pb = np.array(( screen[0], -screen[1], 0))
        pc = np.array((-screen[0],  screen[1], 0))
        pe = cam
        # Compute an orthonormal basis for the screen.
        vr = pb - pa
        vr /= np.linalg.norm(vr)
        vu = pc - pa
        vu /= np.linalg.norm(vu)
        vn = np.cross(vr, vu)
        vn /= np.linalg.norm(vn)
        # Compute the screen corner vectors.
        va = pa - pe
        vb = pb - pe
        vc = pc - pe
        # Find the distance from the eye to screen plane.
        d = -np.dot(va, vn)
        # Find the extent of the perpendicular projection.
        l = np.dot(va, vr) * NEAR_Z / d;
        r = np.dot(vr, vb) * NEAR_Z / d;
        b = np.dot(vu, va) * NEAR_Z / d;
        t = np.dot(vu, vc) * NEAR_Z / d;
        # Load the perpendicular projection.
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glFrustum(l, r, b, t, NEAR_Z, -MIN_Z + d);
        # Rotate the projection to be non-perpendicular.
        m = np.array([
            vr[0], vu[0], vn[0],     0,
            vr[1], vu[1], vn[1],     0,
            vr[1], vu[2], vn[2],     0,
                0,     0,     0,     1,
            ])
        glMultMatrixf(m);
        # Move the apex of the frustum to the origin.
        glTranslatef(-pe[0], -pe[1], -pe[2]);
        # Reset modelview matrix
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

def draw_scene():

    def draw_bounds():
        '''
        Dibuja la caja de líneas blancas que es la continuación de la pantalla
        '''
        pass

    draw_line_to_inf(0, 0.3, 0)
    glColor3f(*COLOR_RED)
    draw_cube(0, 0, 0, 1)
    glColor3f(*COLOR_BLUE)
    draw_cube(2, 2, 2, 2)

    glEnable(GL_LIGHTING)
    glDisable(GL_LIGHTING)

def loop(prm, screen, delta_t, window_s):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # poner mejor nombre, porque es tamaño pantalla /2
    window_s_cm = window_s / prm.px_per_cm / 2
    cam_pos = get_cam_from_mouse(window_s)
    set_camera(prm, cam_pos, window_s_cm, window_s)
    draw_scene()

def main(prm, default_prm, args):
    print("Entrado a escena 3D")

    video.init()
    glutInit()
    video.set_mode_3d()
    video.start_loop(
        lambda screen, delta_t, window_w, window_h:
            loop(prm, screen, delta_t, np.array((window_w, window_h)))
    )
