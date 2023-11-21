from Agente import Aspiradora
import pygame as pg
class Entorno():
    def __init__(self):
        self.Aspiradora = Aspiradora("d", (0,0))
        self.Mapa = []
        
        with open("Mapa.txt", "r") as Mapa:
            Filas = Mapa.readlines()
            for Y,Fila in enumerate(Filas):
                self.Mapa.append([])
                for X,Caracter in enumerate(Fila):
                    if Caracter == "0":
                        self.Mapa[Y].append(self.Celda(X,Y,0))
                    elif Caracter == "1":
                        self.Mapa[Y].append(self.Celda(X,Y,1))
                    elif Caracter != "\n":
                        self.Mapa[Y].append(self.Celda(X,Y,0,True))
        Ancho = len(self.Mapa[0])*50
        Alto = len(self.Mapa)*50
        self.Screen = pg.display.set_mode((Ancho,Alto))
        pg.display.set_caption("Aspiradora")
        pg.display.set_icon(pg.image.load("Aspiradora.png"))

    class Celda():
        def __init__(self, x, y, Suciedad,EsPared=False):
            self.x = x
            self.y = y
            self.Suciedad = Suciedad
            self.EsPared = EsPared
            self.Pared = {"u": 0, "d": 0, "l": 0, "r": 0}

    def MostrarMapa(self):
        self.Screen.fill((0,0,0))
        for Fila in self.Mapa:
            for Celda in Fila:
                if Celda.EsPared:
                    pg.draw.rect(self.Screen,(34,177,76), pg.Rect(Celda.x*50,Celda.y*50,50,50))
                    pg.draw.rect(self.Screen,"Black", pg.Rect(Celda.x*50,Celda.y*50,50,50), 1)
                else:
                    pg.draw.rect(self.Screen,"White", pg.Rect(Celda.x*50,Celda.y*50,50,50))
                    pg.draw.rect(self.Screen,"Black", pg.Rect(Celda.x*50,Celda.y*50,50,50), 1)
                    if Celda.Suciedad == 1:
                        pg.draw.circle(self.Screen,(185,122,87),(Celda.x*50+25,Celda.y*50+25),10)

        #Mostrar Aspiradora
        self.Aspiradora.Dibujar(self.Screen)

    def PosicionarAspiradora(self):
        import random
        Validas = []
        for Fila in self.Mapa:
            for Celda in Fila:
                if not Celda.EsPared:
                    Validas.append(Celda)
        celda = random.choice(Validas)
        self.Aspiradora.Posicion = (celda.x,celda.y)
        self.Aspiradora.Sensores(celda)

    def Actualizar(self):
        pg.display.update()

pg.init()
EntornoReal = Entorno()
EntornoReal.PosicionarAspiradora()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    EntornoReal.MostrarMapa()
    EntornoReal.Actualizar()