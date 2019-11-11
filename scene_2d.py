'''
Funciones relacionadas a pygame para el dibujado de una escena 2D
'''

import video

import pygame
import numpy as np

from config import prm

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

class Image:

    def __init__(
        self,
        path,
        img_pos,
        scaling_factor,
        move_ratio,
        window_s,
        scroll_path = None,
        x_threshold = None,
        scroll_pos = None
    ):
        '''
        Carga una imagen y le da los valores relevantes para el dibujado

        Representa a por ejemplo un prócer que consiste de una imagen de si
        mismo pero además contiene un 'scroll' que es otra imagen arriba que
        viene a ser un cartel con una descripción

        Los últimos argumentos son opcionales ya que pueden haber instancias que
        no tienen cartel o 'scroll', por ejemplo la imagen de fondo

        Argumentos:

        - path (string): Ruta a la imagen relativo al proyecto, generalmente es
          './res/*.jpg'

        - img_pos (tuple): Posición de dibujado, relativo al tamaño de la
          pantalla

        - scaling_factor (float): Ancho de la imagen, en relación con el ancho
          de la pantalla. Normalmente un número menor a 1. Se utiliza para
          escalar la imagen antes de dibujar, el escalado mantendrá la relación
          de aspecto de la imagen original

        - move_ratio (float): Factor de movimiento de la imagen en relación a la
          posición de la cabeza. A mayor factor da sensación de mayor
          profundidad

        - scroll_path (string): Ruta a la imagen de cartel a poner sobre la
          cabeza, relativo al proyecto, generalmente es './res/*.jpg'

        - x_threshold (tuple): Tuple con (min, max), en donde cada número está
          entre 0 y 1. Indica el intervalo en el eje X en donde tiene que estar
          ubicada la posición de la cara detectada para mostrar el scroll o
          cartel sobre la cabeza de este procer

        - scroll_pos (tuple): Posición de dibujado de scroll o cartel sobre la
          cabeza, similar a img_pos.
        '''

        self.path = path
        self.img_pos = img_pos
        self.scaling_factor = scaling_factor
        self.move_ratio = move_ratio
        self.scroll_path = scroll_path
        self.x_threshold = x_threshold
        self.scroll_pos = scroll_pos
        self.scroll_alpha = 0

        image = pygame.image.load(path).convert_alpha()
        _, _, img_w, img_h= image.get_rect()

        # Nuevo tamaño en píxeles
        width = int(window_s[0] * scaling_factor)
        height = int((width / img_w) * img_h)
        self.scaled_img = pygame.transform.scale(image, (width, height))
        self.scaled_img_size = np.array(self.scaled_img.get_rect().size)

        # En el caso que incluya un scroll
        if (scroll_path):
            scroll_img = pygame.image.load(scroll_path).convert_alpha()
            _, _, img_w, img_h = scroll_img.get_rect()

            # Nuevo tamaño en píxeles
            scroll_w = int(window_s[0] * 0.15)
            scroll_h = int((scroll_w / img_w) * img_h)
            self.scaled_scroll = pygame.transform.scale(scroll_img, (scroll_w, scroll_h))
            self.scaled_scroll_size = np.array(self.scaled_scroll.get_rect().size)

    def draw(self, face_pos, window_s, screen, delta_t):
        '''
        Dibuja la imagen en una posición que depende de la posición de la cara

        Toma como argumento la posición normalizada de la cara (aproximadamente
        entre -1 y 1) y la usa para mover levemente la posicón original de la
        imagen y dar efecto de paralaje

        Dar posición y tamaño de pantalla como np.ndarray
        '''
        # Multiplicar posición de cabeza por una cierta sensibilidad, mientras
        # mayor es la sensibilidad da la sensación que las imagenes están a
        # mayor profundidad
        face_pos = face_pos * prm['scene_2d_sensibility']

        # Posicion donde se dibujaria la imagen en píxeles si no hubiera
        # movimiento
        centered_pos = window_s * self.img_pos - self.scaled_img_size / 2

        # Posición donde se dibujará la imagen en pixeles
        pos = centered_pos + self.move_ratio * face_pos * window_s

        # Dibujar imagen
        screen.blit(self.scaled_img, pos)

        # En el caso que incluya un scroll
        if (self.x_threshold):
            # Posicion donde se dibujaria el scroll en píxeles si no hubiera
            # movimiento
            centered_scroll_pos = window_s * self.scroll_pos - self.scaled_scroll_size / 2

            # Posicion donde se dibujará al scroll en pixeles
            scroll_pos = centered_scroll_pos + self.move_ratio * face_pos * window_s

            # Disminuir o aumentar alpha del scroll dependiendo si se está
            # dentro de los límites o no.
            alpha_per_sec = prm['scene_2d_alpha_per_sec']
            # Convertir posición normalizada (entre -1 y 1) a valores utilizados
            # para los límites (entre 0 y 1). Esto es algo aproximado a ojo
            x_pos = face_pos[0] + 0.5
            if (self.x_threshold[0] < x_pos < self.x_threshold[1]):
                self.scroll_alpha += alpha_per_sec * delta_t
                self.scaled_scroll.set_alpha(self.scroll_alpha)
                if self.scroll_alpha > 255:
                    self.scroll_alpha = 255
            else:
                self.scroll_alpha -= alpha_per_sec * delta_t
                self.scaled_scroll.set_alpha(self.scroll_alpha)
                if self.scroll_alpha < 0:
                    self.scroll_alpha = 0

            # Dibujar scroll
            screen.blit(self.scaled_scroll, scroll_pos)

def load_images(window_s):
    '''
    Cargar imágenes de la escena en una lista
    '''
    return [
        Image(
            "./res/casa_tucuman.jpg",
            img_pos=(0.5, 0.65),
            scaling_factor=1.9,
            move_ratio=0.55,
            window_s=window_s
        ),
        Image(
            "./res/moreno.png",
            img_pos=(1.08, 0.8),
            scaling_factor=0.15,
            move_ratio=0.45,
            window_s=window_s
        ),
        Image(
            "./res/paso.png",
            img_pos=(1, 0.8),
            scaling_factor=0.2,
            move_ratio=0.45,
            window_s=window_s,
            scroll_path="./res/scroll_paso.png",
            x_threshold=(2/15, 3/15),
            scroll_pos=(1.025, 0.3)
        ),
        Image(
            "./res/larrea.png",
            img_pos=(-0.05, 0.85),
            scaling_factor=0.3,
            move_ratio=0.45,
            window_s=window_s,
            scroll_path="./res/scroll_larrea.png",
            x_threshold=(13/15, 14/15),
            scroll_pos=(-0.05, 0.35)
        ),
        Image(
            "./res/matheu.png",
            img_pos=(0.08, 0.8),
            scaling_factor=0.3,
            move_ratio=0.4,
            window_s=window_s,
            scroll_path="./res/scroll_matheu.png",
            x_threshold=(12/15, 13/15),
            scroll_pos=(0.08, 0.3)
        ),
        Image(
            "./res/alberti.png",
            img_pos=(0.85, 0.8),
            scaling_factor=0.3,
            move_ratio=0.35,
            window_s=window_s,
            scroll_path="./res/scroll_alberti.png",
            x_threshold=(3/15, 4/15),
            scroll_pos=(0.85, 0.3)
        ),
        Image(
            "./res/azcuenaga.png",
            img_pos=(0.2, 0.8),
            scaling_factor=0.3,
            move_ratio=0.35,
            window_s=window_s,
            scroll_path="./res/scroll_azcuenaga.png",
            x_threshold=(11/15, 12/15),
            scroll_pos=(0.2, 0.3)
        ),
        Image(
            "./res/belgrano.png",
            img_pos=(0.7, 0.75),
            scaling_factor=0.3,
            move_ratio=0.3,
            window_s=window_s,
            scroll_path="./res/scroll_belgrano.png",
            x_threshold=(4/15, 5/15),
            scroll_pos=(0.7, 0.25)
        ),
        Image(
            "./res/castelli.png",
            img_pos=(0.3, 0.75),
            scaling_factor=0.3,
            move_ratio=0.25,
            window_s=window_s,
            scroll_path="./res/scroll_castelli.png",
            x_threshold=(10/15, 11/15),
            scroll_pos=(0.3, 0.25)
        ),
        Image(
            "./res/saavedra.png",
            img_pos=(0.5, 0.9),
            scaling_factor=0.5,
            move_ratio=0.2,
            window_s=window_s,
            scroll_path="./res/scroll_saavedra.png",
            x_threshold=(7/15, 9/15),
            scroll_pos=(0.45, 0.2)
        ),
    ]

def demo():
    print("Entrado a escena 2D")
    print("Mover mouse para hacer paralaje")

    v = video.Video()
    v.set_mode_2d()

    window_s = np.array(v.screen_size)

    images = load_images(window_s)

    def loop(screen, delta_t, window_w, window_h):

        screen.fill(COLOR_BLACK)

        # Simular posición normalizada de cara a partir del mouse
        mouse = np.array(pygame.mouse.get_pos())
        face_pos = (mouse - window_s / 2) / window_s

        for image in images:
            image.draw(face_pos, window_s, screen, delta_t)

    v.start_loop(loop)
