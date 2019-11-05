# parallax-portal

Basado en:

- https://github.com/agirault/screenReality

- http://csc.lsu.edu/~kooima/pdfs/gen-perspective.pdf

- https://www.youtube.com/watch?v=SWt_y5uIEAo

- Tutoriales OpenGL:

  - http://pyopengl.sourceforge.net/context/tutorials/index.html

  - https://learnopengl.com/

  - https://www.opengl-tutorial.org/beginners-tutorials/tutorial-2-the-first-triangle/

  - https://stackoverflow.com/questions/24416589/glsl-using-custom-output-attribute-instead-of-gl-position

  - https://gist.github.com/binarycrusader/5823716a1da5f0273504

  - https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/6.pbr/1.2.lighting_textured/lighting_textured.cpp

Inspirado en:

- https://gitlab.kitware.com/mike.rye/paraview_face_tracking

- https://github.com/DhananjaiH/Head-tracking

- http://johnnylee.net/projects/wii/

- https://youtu.be/Jd3-eiid-Uw?t=214

- https://www.youtube.com/watch?v=bBQQEcfkHoE

- https://www.youtube.com/watch?v=h5QSclrIdlE&

Herramientas:

- https://christopherchudzicki.github.io/MathBox-Demos/parametric_curves_3D.html

- https://www.cs.utexas.edu/~teammco/misc/kalman_filter/

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

Despues para iniciar el programa posta:

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

- `scroll.png`: Pizabay license: https://pixabay.com/vectors/scrolls-rolls-papyrus-papers-34607/

- Skybox: Ivar Leidus [CC BY-SA 3.0 ee (https://creativecommons.org/licenses/by-sa/3.0/ee/deed.en)] https://commons.wikimedia.org/wiki/File:Suurupi_alumine_tuletorn_panoraam.jpg

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

- Disminuir tembleque, ver si ponerle como inercia a la posicion de la camara
  para que cuando pierda detección siga moviendose hacia donde iba y lentamente
  se vaya centrando. Filtrar un poco la ubicación de la cámara con Kalman o al
  menos un promedio de las últimas 5 posiciones metele

- Hacer que scene2d reciba la posición de la cara en unidades adimensionales (ni
  pixeles ni cm) y agregar un prm que sea la sensibilidad

- Ver que hacer para pasar de escena a escena, por ejemplo al detectar
  movimiento de la mano al frente de la camara

- Ver si estamos usando el XML del haarcascade correcto

- Documentar de que es importante que haya luz de frente

- Terminar de hacer lo del scroll, con transicion de transparencia, o de ultima
  ni hacerlo

- Si va al museo, poner un mensaje que diga algo de "No hay caras detectadas,
  acercarse para ver el efecto, una persona a la vez"

- Hacer configurable en prm la ubicación de la camara respecto al centro de la
  pantalla.

- En parallax calcular posicion en cm a partir de posicion en pixeles y del f
  de la camara que tambien tiene que ser configurable

- Al terminar parallax borrar codigo C++

- Documentar que instalar GLM y OpenGL no es tan facil

- Hacer mas linda la escena 3d

- Buscar imagenes temáticas

## Preguntar

- Posibilidad de comprar una PC Mini ITX y hasta cuánto gastar
