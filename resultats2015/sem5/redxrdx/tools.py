# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:09:00 2016

@author: 3200404
"""

from soccersimulator import SoccerAction
from soccersimulator import Vector2D
from soccersimulator import settings
import math
import random



def miroir_p(p):       # miroir position
    return Vector2D( settings.GAME_WIDTH - p.x,p.y)

        # miroir vecteur
def miroir_v(v):
    return Vector2D(-1*v.x , v.y)  
    
def miroir_sa(action):
    return SoccerAction(miroir_v(action.acceleration),miroir_v(action.shoot))
    
def miroir_st(state):
    res = state.copy()
    res.ball.position = miroir_p(state.ball.position)
    res.ball.vitesse = miroir_v(state.ball.vitesse)
    for (id_team, id_player) in state.players :
        (res.player_state(id_team,id_player)).position = miroir_p(state.player_state(id_team,id_player).position)
        (res.player_state(id_team,id_player)).vitesse = miroir_v(state.player_state(id_team,id_player).vitesse)
    return res    
    
    
class PlayerDecorator :
    
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    def position_joueur(self):
          return self.state.player_state(self.id_team, self.id_player).position  

    def position_balle(self):
        return self.state.ball.position
        
        
    def balle_chez_adv(self):
        if (self.position_balle().x > settings.GAME_WIDTH / 2):
            return True
        else:
            return False
  
    def chercher_balle(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.non_tir())
    
    
    def possede_balle(self):
        if(self.position_balle() == self.position_joueur() ) :
          return 1
        
    def balle_chez_nous(self):
         if (self.position_balle().x < settings.GAME_WIDTH / 2):
            return True
         else:
            return False
    
    def tirer(self):
       
       
       if (self.position_balle().y > settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,-(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       if (self.position_balle().y < settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       return Vector2D(settings.GAME_HEIGHT,0)
        
    def non_tir (self) :
        return Vector2D(0,0);
    
        
    def position_but_adv(self):
        return (Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2))
      
    def degage(self):
        return Vector2D(settings.GAME_HEIGHT,20)

    def degage_alea(self):
        return Vector2D(settings.GAME_HEIGHT,random.randrange(settings.GAME_HEIGHT/3,(2*settings.GAME_HEIGHT)/3))

    def marquer(self):
        return SoccerAction(self.position_balle() - self.position_joueur() , self.tirer())
        
    def conserver(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.non_tir())
    
    def degager(self):
        return SoccerAction(self.position_balle() - self.position_joueur(),self.degage_alea())
        
    def positionG(self):
        return SoccerAction((Vector2D(10,settings.GAME_HEIGHT/2))-self.position_joueur(), self.tirer())
    
    def defendre (self):
        return SoccerAction(self.position_balle() - self.position_joueur(),self.degage())
    
    
    def suivre_jeu(self):
        return SoccerAction(Vector2D(settings.GAME_WIDTH /3,self.position_balle().y)-self.position_joueur(), self.tirer())
        
    def defense(self):
        v= Vector2D(settings.GAME_WIDTH*1/5,settings.GAME_HEIGHT/2.)
        return self.retour_position(v)
    
    def retour_position(self, v):
         return SoccerAction(v - self.position_joueur(),Vector2D())
         
         
    def distanceAll(self):
        v = self.state.player(1,0).position 
        w = self.state.player(1,1).position
        return v.distance(w)
        
    def distanceAdv(self):
        v = self.position_joueur  
        w = self.state.player(2,1).position
        return v.distance(w)
        
    def distanceBalle(self):
    
     i=1
     j=0
     for i in range(1,self.id_team) :
        for j in range(0,self.id_player):
         
           v = self.state.player(i,j).position 
           w = self.position_balle
        if v.distance(w) < 10 :
        
            return  self.state.player(i,j)
        j = j+1         
     i = i+1
     
     return 0
     
     
    def sortieGardien(self) :
         if( self.position_balle().x < settings.GAME_WIDTH / 6 ) :
             return 1
             
    def zone_de_tir(self) :
         if( self.position_balle().x > settings.GAME_WIDTH / 6 ) :
             return 1         
       
    def dans_perimetre(self) :
        if (self.position_balle().y > settings.GAME_HEIGHT/3 and self.position_balle().y < (settings.GAME_HEIGHT*2) / 3) :
            return 1
         
   