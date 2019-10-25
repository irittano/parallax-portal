'''
Funciones relacionadas a OpenGL para el dibujado de una escena 3D
'''

import video

from OpenGL.GL import *
from OpenGL.GLU import *

def main(prm, default_prm, args):
    print("Entrado a escena 3D")

    w,h= 500,500
    def square():
        glBegin(GL_QUADS)
        glVertex2f(100, 100)
        glVertex2f(200, 100)
        glVertex2f(200, 200)
        glVertex2f(100, 200)
        glEnd()

    def iterate():
        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def showScreen(_):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate()
        glColor3f(1.0, 0.0, 3.0)
        square()
        #  video.update()

    video.init()
    video.set_mode_3d()
    video.start_loop(showScreen)
