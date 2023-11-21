import pygame as pg
from Entorno import Entorno

pg.init()
EntornoReal = Entorno()
EntornoReal.CreacionMapaTxt(100,100)
EntornoReal.CreacionCeldas()
EntornoReal.CreacionMapaVentana()
EntornoReal.PosicionarAspiradora()
Velocidad = 50
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if Velocidad > 1:
                    Velocidad -= 10
            elif event.key == pg.K_LEFT :
                if Velocidad < 1000:
                    Velocidad += 10
            elif event.key == pg.K_SPACE:
                Velocidad *= -1
    EntornoReal.MostrarMapa()
    EntornoReal.MoverAspiradora()
    if Velocidad > 1:
        pg.time.delay(Velocidad)
    EntornoReal.Actualizar()