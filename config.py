'''
Archivo con configuraciones o parámetros

Este código se ejecuta solamente la primera vez que se importa este módulo,
entonces cuando main.py haga "from config import prm" el objeto "prm" se va a
crear. Cuando otro módulo como video.py haga lo mismo, en vez de crearse otro
"prm" se le va a dar una referencia al objeto creado previamente. De esta forma
todos los módulos pueden acceder a este mismo objeto como si fuera una variable
global

Tambien creo "default_prm" que mantiene los parametros por defecto, los
mantenemos ahí para tener como referencia y saber cuales cambiamos en "prm".
Este objeto no deberia ser modificado nunca
'''

class Parameters:
    def __init__(self):
        '''
        Objeto que mantiene todas los parámetros o opciones

        Objeto que mantiene todos los parametros configurables del programa,
        permite tener todo en un solo lugar para luego cambiarlos durante la
        ejecucion del programa

        Tener en cuenta que algunos parámetros solo son leídos al iniciar el
        programa, por ejemplo la resolución de pantalla. En esos casos hay que
        cerrar el programa, cambiar el valor acá en este archivo y volver a
        abrirlo

        Mantiene el valor de cada parámetro y una descripción por las dudas.
        Tambien mantiene un valor mínimo, uno máximo y un incremento para usar
        cuando se cambia el valor usando el teclado. Ver video.py
        '''

        self.parameters = {
            "face_detection_min_size": {
                "descr": "Tamaño minimo de cara detectada",
                "val": 30, "min": 5, "max": 1000, "step": 1,
            },
            "face_detection_min_neighbors": {
                "descr": "Cantidad de caras minimas a detectar para considerar \
                    deteccion positiva",
                "val": 15, "min": 1, "max": 50, "step": 1,
            },
            "face_detection_scale_factor": {
                "descr": "En cuanto agrandar tamaño de cara buscada en cada \
                    paso de la deteccion",
                "val": 1.02, "min": 1.05, "max": 2, "step": 0.5,
            },
            "camera_device_index": {
                "descr": "Numero de camara a usar para la deteccion de caras",
                "val": 0, "min": 0, "max": 4, "step": 1,
            },

            "video_show_fps": {
                "descr": "Si mostrar FPS",
                "val": True,
            },
            "video_show_prm": {
                "descr": "Si mostrar estos parametros para permitir \
                    modificaciones",
                "val": True,
            },

            "scene_3d_perspective": {
                "descr": "Si usar gluPerspective para pruebas en lugar de \
                    glFrustum",
                "val": False,
            },
            "scene_3d_grid_size": {
                "descr": "Separacion de grilla en cm",
                "val": 3, "min": 0.5, "max": 30, "step": 0.5,
            },

            "screen_auto_size": {
                "descr": "Si usar máximo tamaño de pantalla disponible",
                "val": True,
            },
            "screen_w": {
                "descr": "Ancho de pantalla a usar si no es automático",
                "val": 1920, "min": 100, "max": 10000, "step": 10,
            },
            "screen_h": {
                "descr": "Alto de pantalla a usar si no es automático",
                "val": 1080, "min": 100, "max": 10000, "step": 10,
            },
            "px_per_cm": {
                "descr": "Algo asi como DPI pero en centimetros",
                "val": 44, "min": 10, "max": 200, "step": 0.5,
            },
        }

    def __getitem__(self, key):
        '''
        Para acceder a los parámetros

        Haciendo por ejemplo:

            ancho = prm["screen_w"]
        '''
        return self.parameters[key]["val"]

    def __setitem__(self, key, value):
        '''
        Para modificar los parámetros

        Haciendo por ejemplo:

            prm["screen_w"] = 1080
        '''
        self.parameters[key]["val"] = value

    def __iter__(self):
        '''
        Para iterar sobre cada parámetro

        Haciendo por ejemplo:

            for index, key in enumerate(prm):
                print("Opcion N° {}, {} = {}".format(index, key, prm[key]))
        '''

        return iter(self.parameters)

    def __len__(self):
        '''
        Para obtener cantidad de parámetros
        '''

        return len(self.parameters)

    def increment(self, key):
        '''
        Usado por video.py para incrementar el valor usando el teclado

        Si el parámetro es True o False se va a invertir, si el parámetro es un
        número se va a aumentar el valor
        '''
        prm = self.parameters[key]
        if type(prm["val"]) == bool:
            prm["val"] = not prm["val"]
        else:
            prm["val"] += prm["step"]
            if prm["val"] > prm["max"]:
                prm["val"] = prm["max"]

    def decrement(self, key):
        '''
        Usado por video.py para disminuir el valor usando el teclado

        Si el parámetro es True o False se va a invertir, si el parámetro es un
        número se va a disminuir el valor
        '''
        prm = self.parameters[key]
        if type(prm["val"]) == bool:
            prm["val"] = not prm["val"]
        else:
            prm["val"] -= prm["step"]
            if prm["val"] < prm["min"]:
                prm["val"] = prm["min"]

prm = Parameters()
default_prm = Parameters()
