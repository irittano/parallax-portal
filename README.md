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

### Dependencias

- OpenCV 2.4.10 : `sudo apt install libopencv-dev`

- OpenGL & freeGLUT : `sudo apt install libxi-dev libxmu-dev freeglut3-dev`

### Ejecución

```
mkdir build
cd build
cmake ..
make
./bin/screenReality
```

### Atajos de teclado

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

- Optimizar detección de cara para minimizar el delay

- Revisar cómo se calcula posición del frustum de la perspectiva y corregirlo

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
