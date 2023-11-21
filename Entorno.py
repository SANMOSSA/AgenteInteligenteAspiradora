from Agente import Aspiradora
import pygame as pg
class Entorno():
    def __init__(self):
        self.Aspiradora = Aspiradora("d", (0,0),100)
        self.Mapa = []
        self.BateriaImagen = pg.image.load("Bateria.png")
        self.CeldasSucias = 0

    def CreacionMapaTxt(self,Columnas,Filas):
        import random
        if Columnas < 10:
            Columnas = 10
        if Filas < 10:
            Filas = 10
        if Columnas > 30:
            Columnas = 30
        if Filas > 18:
            Filas = 18
        with open("Mapa.txt", "w") as Mapa:
            for Y in range(Filas):
                for X in range(Columnas):
                    if Y == 0 or Y == Filas-1 or X == 0 or X == Columnas-1:
                        Mapa.write("2")
                    else:
                        #Tres opciones, 0: Limpio, 1: Sucio, 2: Pared, la probabilidad de que sea sucio es de 4/10, de que sea pared es de 2/10 y de que sea limpio es de 4/10
                        Opcion = random.randint(1,100)
                        if Opcion <= 40:
                            Mapa.write("0")
                        elif Opcion <= 80:
                            Mapa.write("1")
                        else:
                            Mapa.write("2")
                Mapa.write("\n")

    def CreacionMapaVentana(self):
        Ancho = (len(self.Mapa[0])-1)*50
        Alto = len(self.Mapa)*50 + 50*2
        self.Screen = pg.display.set_mode((Ancho,Alto))
        pg.display.set_caption("Aspiradora")
        pg.display.set_icon(pg.image.load("Aspiradora.png"))

    def CreacionCeldas(self):
        with open("Mapa.txt", "r") as Mapa:
            Filas = Mapa.readlines()
            for Y,Fila in enumerate(Filas):
                self.Mapa.append([])
                for X,Caracter in enumerate(Fila):
                    #Tipo de celda
                    if Caracter == "0":
                        _Celda =  self.Celda(X,Y,0)
                    elif Caracter == "1":
                        _Celda =  self.Celda(X,Y,1)
                        self.CeldasSucias += 1
                    elif Caracter != "\n":
                        _Celda =  self.Celda(X,Y,0,True)

                    if 0 < Y < len(Filas)-1 and 0 < X < len(Fila)-1 and Caracter != "\n" and Caracter != "2":
                        if Filas[Y-1][X] == "2":
                            _Celda.Pared["u"] = 1
                        if Filas[Y+1][X] == "2":
                            _Celda.Pared["d"] = 1
                        if Fila[X-1] == "2":
                            _Celda.Pared["l"] = 1
                        if Fila[X+1] == "2":
                            _Celda.Pared["r"] = 1
                    self.Mapa[Y].append(_Celda)
            self.Aspiradora.BateriaBase = len(Filas)*len(Filas[0])*5
            self.Aspiradora.Bateria = self.Aspiradora.BateriaBase

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
                
                #Mostrar Paredes
                if Celda.Pared["u"] == 1:
                    pg.draw.line(self.Screen,"Black",(Celda.x*50,Celda.y*50),(Celda.x*50+50,Celda.y*50),5)
                if Celda.Pared["d"] == 1:
                    pg.draw.line(self.Screen,"Black",(Celda.x*50,Celda.y*50+50-2),(Celda.x*50+50,Celda.y*50+50-2),5)
                if Celda.Pared["l"] == 1:
                    pg.draw.line(self.Screen,"Black",(Celda.x*50,Celda.y*50),(Celda.x*50,Celda.y*50+50),5)
                if Celda.Pared["r"] == 1:
                    pg.draw.line(self.Screen,"Black",(Celda.x*50+50-2,Celda.y*50),(Celda.x*50+50-2,Celda.y*50+50),5)


        #Mostrar Aspiradora
        self.Aspiradora.Dibujar(self.Screen)
        #Dibujar la carga de la bateria
        Bateria = self.Aspiradora.Bateria
        Porcentaje = round(Bateria*100/self.Aspiradora.BateriaBase)
        Valor = (250)*Porcentaje/100
        pg.draw.rect(self.Screen,(57,152,83), pg.Rect(0,len(self.Mapa)*50,Valor,100))
        self.Screen.blit(self.BateriaImagen,(0,len(self.Mapa)*50))
        Texto = pg.font.SysFont("Arial", 100).render(str(Porcentaje), True, "White")
        self.Screen.blit(Texto,(50,len(self.Mapa)*50-5))
        Texto = pg.font.SysFont("Arial", 100).render(str(self.CeldasSucias), True, "White")
        self.Screen.blit(Texto,(300,len(self.Mapa)*50-5))

        if self.Aspiradora.LLegoObjetivo():
            Texto = pg.font.SysFont("Arial", 100).render(str("Termino"), True, "Black")
            self.Screen.blit(Texto,(self.Screen.get_width()/2-Texto.get_width()/2,self.Screen.get_height()/2-Texto.get_height()/2))

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

    def MoverAspiradora(self):
        celda = self.Mapa[self.Aspiradora.Posicion[1]][self.Aspiradora.Posicion[0]]
        self.Aspiradora.Sensores(celda)
        if celda.Suciedad == 1 and bool(self.Aspiradora.Aspirar()):
            self.Mapa[self.Aspiradora.Posicion[1]][self.Aspiradora.Posicion[0]].Suciedad = 0
            self.CeldasSucias -= 1
        self.Aspiradora.Mover()

    def Actualizar(self):
        pg.display.update()

