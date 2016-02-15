import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from random import *

class zone(object):
    def __init__(self,bg,hd):
        self.bg = bg
        self.hd = hd
        
#La normalisation permet de se placer dans le cadre d'un carre  (-1,-1)  (1,1) de cot 2
    def normalisation(self,Vecteur):
        Vecteur.x = (Vecteur.x * 2 / self.hd.x - self.bg.x) - 1
        Vecteur.y = (Vecteur.y * 2 / self.hd.y - self.bg.y) - 1
        return Vecteur

#renvoi les vecteurs aux proportion de la zone initiale
    def denormalisation(self, Vecteur):
        Vecteur.x = (Vecteur.x + 1)* (self.hd.x + self.bg.x) / 2
        Vecteur.y = (Vecteur.y + 1)* (self.hd.y + self.bg.y) / 2
        return Vecteur
    
    def est_dans(self,pos):
        if (pos.x <= self.bg.x or pos.x >= self.hd.x):
            return False
        if (pos.y <= self.bg.y or pos.y >= self.hd.y):
            return False
        return True

    def vecteur_dans_zone(self,v):
        if(v.x > self.bg.x and v.x < self.hd.x and v.y > self.bg.y and v.y < self.hd.y):
            return True
        else:
            return False
    

    #important
    def mirroir(self,Vecteur):
        V = self.normalisation(Vecteur)
        V.x = -(V.x)
        V = self.denormalisation(Vecteur)
        return V

    @property
    def zone_mirroir(self):
        c1 = Vector2D(0,-1)
        c2 = Vector2D(1,1)
        c1 = self.denormalisation(c1)
        c2 = self.denormalisation(c2)
        return zone(c1,c2)

    @property
    def division_verticale(self):
        #zone droite
        c1 = Vector2D(0,-1)
        c2 = Vector2D(1,1)
        c1 = self.denormalisation(c1)
        c2 = self.denormalisation(c2)

        #zonegauche
        c3 = Vector2D(-1,-1)
        c4 = Vector2D(0,1)
        c3 = self.denormalisation(c3)
        c4 = self.denormalisation(c4)
        L = []
        L.append(zone(c3,c4))
        L.append(zone(c1,c2))
        return L

    @property
    def division_horizontale(self):
        #zone haut
        c1 = Vector2D(-1,-0)
        c2 = Vector2D(1,1)
        c1 = self.denormalisation(c1)
        c2 = self.denormalisation(c2)

        #zone bas
        c3 = Vector2D(-1,-1)
        c4 = Vector2D(1,0)
        c3 = self.denormalisation(c3)
        c4 = self.denormalisation(c4)
        L = []
        L.append(zone(c3,c4))
        L.append(zone(c1,c2))
        return L
        

    @property
    def milieu(self):
        return self.denormalisation(Vector2D(0,0))

    def distance(self,vecteur):
        return distance(self.milieu,vecteur)

    @property
    def alea(self):
        x = random()*2 - 1
        y = random()*2 - 1
        return self.denormalisation(Vector2D(x,y))

    

terrain = zone(Vector2D(0,0),Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT))
z = terrain.division_verticale
gauche = z[0]
droite = z[1]
bg_milieu = terrain.denormalisation(Vector2D(-0.5,-1))
hd_milieu = terrain.denormalisation(Vector2D(0.5,1))
m = zone(bg_milieu,hd_milieu)

