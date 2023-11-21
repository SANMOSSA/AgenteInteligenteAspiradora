import pygame as pg
class Aspiradora():
    def __init__(self, Direccion, Posicion):
        self.Direccion = Direccion # "u", "d", "l", "r"
        self.Posicion = Posicion
        self.Bateria = 100
        self.ImagenLimpia = pg.image.load("Aspiradora.png")
        self.ImagenSucia = pg.image.load("AspiradoraSucia.png")
        self.SU = 0
        self.PR = 0
        self.CB = 1
        self.Objetivo = {"SU": 0, "PR": 0, "CB": 0}
        self.Moviendo = False

    def Sensores(self,Celda):
        self.SU = Celda.Suciedad
        self.PR = Celda.Pared[self.Direccion]
        if self.Bateria > 1:
            self.CB = 1
        else:
            self.CB = 0 

    def Motor(self):
        if self.SU == 1 and self.PR == 1 and self.CB == 1:
            return "qu"
        elif self.SU == 1 and self.PR == 1 and self.CB == 0:
            return "qu"
        elif self.SU == 1 and self.PR == 0 and self.CB == 1:
            return "qu"
        elif self.SU == 1 and self.PR == 0 and self.CB == 0:
            return "qu"
        elif self.SU == 0 and self.PR == 1 and self.CB == 1:
            return "de"
        elif self.SU == 0 and self.PR == 1 and self.CB == 0:
            return "qu"
        elif self.SU == 0 and self.PR == 0 and self.CB == 1:
            self.CB -= 1
            return "ad"
        elif self.SU == 0 and self.PR == 0 and self.CB == 0:
            return "qu"
        else:
            return "qu"
        
    def Aspirar(self):
        if self.SU == 1 and self.CB == 1:
            self.CB -= 1
            return 1
        else:
            return 0

    def Dibujar(self, Screen):
        # Gira la imagen de la aspiradora
        if self.Moviendo:
            if self.Direccion == "u":
                self.ImagenLimpia = pg.transform.rotate(self.ImagenLimpia, 0)
                self.ImagenSucia = pg.transform.rotate(self.ImagenSucia, 0)
            elif self.Direccion == "d":
                self.ImagenLimpia = pg.transform.rotate(self.ImagenLimpia, 180)
                self.ImagenSucia = pg.transform.rotate(self.ImagenSucia, 180)
            elif self.Direccion == "l":
                self.ImagenLimpia = pg.transform.rotate(self.ImagenLimpia, 90)
                self.ImagenSucia = pg.transform.rotate(self.ImagenSucia, 90)
            elif self.Direccion == "r":
                self.ImagenLimpia = pg.transform.rotate(self.ImagenLimpia, 270)
                self.ImagenSucia = pg.transform.rotate(self.ImagenSucia, 270)

        if self.SU == 1:
            Screen.blit(self.ImagenSucia, (self.Posicion[0]*50,self.Posicion[1]*50))
        else:
            Screen.blit(self.ImagenLimpia, (self.Posicion[0]*50,self.Posicion[1]*50))