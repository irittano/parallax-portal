# parallax-portal

Basado en:

- https://github.com/agirault/screenReality

- http://csc.lsu.edu/~kooima/pdfs/gen-perspective.pdf

- https://www.youtube.com/watch?v=SWt_y5uIEAo

Inspirado en:

- https://gitlab.kitware.com/mike.rye/paraview_face_tracking

- https://github.com/DhananjaiH/Head-tracking

- http://johnnylee.net/projects/wii/

- https://youtu.be/Jd3-eiid-Uw?t=214

- https://www.youtube.com/watch?v=bBQQEcfkHoE

- https://www.youtube.com/watch?v=h5QSclrIdlE&

## Dependencias Python

Usar Pipenv:

```
pipenv install
```

Sino se puede instalar con `pip3` cada dependencia que aparece en el archivo
`Pipfile`

## Ejecucion de Python

Si se usa Pipenv primero hacer:

```
pipenv shell
```

Despues para inicial el programa posta:

```
./main.py parallax
```

Para probar las distintas partes puede hacer

```
./main.py scene_3d
./main.py face_detection
...
```

## Estructura Python

Hay varios archivos, la idea es que `main.py` dependiendo de los argumentos
inicie el programa posta en el `main()` de `parallax.py` o ejecute funciones
`main()` en distintos modulos. De esa forma cada modulo tiene una "demo" o una
prueba cortita para ver que anda lo que esta ahi adentro. Cada uno puede
trabajar en esa demo sin pisarse y mas adelante hacemos `parallax.py` que
integre todo

- `main.py`: Es el punto de inicio, el programa se ejecuta desde aca.

- `parallax.py`: Importa todos los modulos y usa las funciones de todos los
  demas archivos, tiene una funcion `main()` que corre el programa en serio.

- `video.py`: Maneja la ventana, pygame y las cosas basicas de OpenGL

- `scene_3d.py`: Tiene las funciones de dibujado para OpenGL y en su `main()`
  tiene una demo que al menos muestra algo para verificar que anda OpenGL

- `scene_2d.py`: Tiene las funciones de dibujado 2D en pygame y en su `main()`
  tiene una demo que al menos muestra algo para verificar que anda pygame

- `face_detection.py`: Tiene las funciones de deteccion de cara en OpenCV y en
  su `main()` tiene una demo que al menos muestra algo para verificar que anda
  OpenCV

## Atribuciones

- Estampillas: Dominio público: https://commons.wikimedia.org/wiki/Stamps_of_Argentina

- `casa_tucuman.jpg`: Fulviusbsas [CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0)]

- `belgrano.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Retrato_del_Gral._Manuel_Belgrano_-_Atribu%C3%ADdo_a_Francois_Casimir_Carbonnier.jpg

- `saavedra.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Cornelio_Saavedra_-_1810.jpg

- `moreno.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Mariano_Moreno.jpg

- `paso.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Juanjpaso.jpg

- `alberti.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Manuel_Alberti_2.jpg

- `azcuenaga.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Miguel-Azcu%C3%A9naga_new.png

- `castelli.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Castelli.jpg

- `matheu.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Retrato_de_Domingo_Matheu.jpg

- `larrea.png`: Dominio público: https://commons.wikimedia.org/wiki/File:Juan_Larrea.jpg

## Dependencias C++

- OpenCV 2.4.10 : `sudo apt install libopencv-dev`

- OpenGL & freeGLUT : `sudo apt install libxi-dev libxmu-dev freeglut3-dev`

## Ejecución C++

```
mkdir build
cd build
cmake ..
make
./bin/screenReality
```

## Detalles C++

- El parametro `pixelNbrPerCm` es el pixeles por centimetro del monitor y hay
  que ajustarlo

- Habia un error en el programa original en donde `cx` y `cy` eran el doble de
  lo que deberían

- Hay que ayustar la posicion de la camara respecto a la pantalla, el programa
  original no lo hacía

- Ayuda que los cuadrados de las paredes sean cuadrados y no rectángulos

- Ayuda mucho poner una caja para continuar el efecto fuera de la pantalla

- Ayuda mucho cerrar un ojo

## Atajos de teclado C++

* **Q** : *Salir*
* **F** : *Pantalla completa*
* **I** : *Invertir imagen de cámara*
* **C** : *Mostrar u ocultar camara*
* **D** : *Mostrar información de detección*
* **+/-** : *Cambiar tamaño de ventana de cámara*
* **M** : *Cambiar PolygonMode entre LINE y FILL*
* **P** : *Cambiar ProjectionMode entre Off-Axis y Regular*
* **B** : *Bounding box display ON/OFF*

## Tareas

- Disminuir tembleque

- Portear a python

- Ver que haarcascade usar

- Revisar cómo se calcula posición del frustum de la perspectiva y corregirlo.
  Un parámetro a ver es pixelNbrPerCm

- Dibujar en 2D imágenes con paralaje para hacer el escenario de una foto de un
  lugar con un prócer

- Dibujar en 2D o 3D una galería de imágenes tipo Polaroid

- Chequear bien el angulo de visión de la camara, ver donde están los puntos
  ciegos cuando te acercás

- Suavizar datos de detección de cara, con un promedio? Kalman?

- Buscar formas de determinar mejor la distancia, a lo mejor usando dos cámaras?
  Viendo distancia entre los ojos? Haciendo que la persona se ponga una gorra
  con pelotitas de colores? Con LEDs infrarrojos?

- Determinar donde poner la TV y la cámara? Poner TV en vertical y una cámara
  justo al costado?

- Separar detección y dibujado en dos threads?

- Soportar monitor 3D?

## Ideas

- Hacer un cuadro de texto arriba a la derecha medio futurista explicando cosas

- Ponerle nombres a los proceres sobre las cabezas

## Preguntar

- En serio lo van a poner en un museo o lo están viendo? Sino lo optimizamos
  para notebooks con webcams

- En dónde estaría ubicado? En contra de una pared? Pasa gente caminando por
  atrás? Habría que marcar el piso para que la gente se de cuenta de
  pasar de a uno?

- Cuáles son los tiempos? Fin de año? Marzo?

- Posibilidad de comprar una PC Mini ITX y hasta cuánto gastar

- Ya tienen televisor?

- Que webcam hay?

- De qué temática son las imágenes? Nos pueden pasar algunas desde el museo?
