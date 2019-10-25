'''
Funciones relacionadas a OpenGL para el dibujado de una escena 3D
'''

import video

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

MAX_Z = -60

def draw_line_to_inf(x, y, z):
    '''
    Dibujar linea desde posicion dada hasta un gran Z
    '''
    glBegin(GL_LINE_LOOP)

    glColor3f(1, 1, 1)
    glVertex3f(x, y, z)
    glColor3f(0, 0, 0)
    glVertex3f(x, y, MAX_Z)

    glEnd()

def draw_cube(x, y, z, w, h, d):
    glColor3f(1, 1, 0)
    glTranslatef(1, 1, 1)
    glutSolidCube(3)
    glTranslatef(-1, -1, -1)

def set_camera(window_w, window_h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, window_w / window_h, 1, 250)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam_x = 0
    cam_y = 0
    cam_z = 0
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

def draw_scene():

    draw_line_to_inf(0, 0.3, 0)
    draw_cube(0, 0, 0, 0, 0, 0)

    glEnable(GL_LIGHTING)
    glDisable(GL_LIGHTING)

def loop(screen, delta_t, window_w, window_h):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    set_camera(window_w, window_h)
    draw_scene()


def main(prm, default_prm, args):
    print("Entrado a escena 3D")

    video.init()
    glutInit()
    video.set_mode_3d()
    video.start_loop(loop)
