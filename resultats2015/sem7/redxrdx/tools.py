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
    
    def distance_balle(self):
        return self.state.player_state(self.id_team, self.id_player).position.distance(self.state.ball.position)     
    
    def cornerX(self):
        if (self.position_balle().x >= settings.GAME_WIDTH-10):
            return 1
        else:
            return 0
        
    def cornerYH(self):
        if( self.position_balle().y >= (settings.GAME_HEIGHT - 10) ):
            return 1
        else:
             return 0
          
    def cornerYB(self):
   
       if(self.position_balle().y <= (settings.GAME_HEIGHT - 80) ):
        return 1
       else :
        return 0
        
        
    def balle_chez_adv(self):
        if (self.position_balle().x >= settings.GAME_WIDTH / 2):
            return True
        else:
            return False
  
    def chercher_balle(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.non_tir())
    
    
    def possede_balle(self):
        if(self.position_balle() == self.position_joueur() ) :
          return 1
        else:
            return 0
        
    def balle_chez_nous(self):
         if (self.position_balle().x < settings.GAME_WIDTH / 2):
            return True
         else:
            return False
    
    def balle_en_def(self):
         if (self.position_balle().x < settings.GAME_WIDTH / 4):
            return 1
         else:
            return 0
      
    def balle_au_mil(self):
         if (self.position_balle().x <= settings.GAME_WIDTH / 2.5 and self.position_balle().x >= settings.GAME_WIDTH / 1.5 ):
            return 1
         else:
            return 0
            
    def tirer(self):
       
      
       if (self.position_balle().y > settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,-(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       if (self.position_balle().y < settings.GAME_HEIGHT/2):
           return Vector2D (settings.GAME_HEIGHT,(self.position_balle().y - settings.GAME_HEIGHT/2))
       
       return Vector2D(settings.GAME_HEIGHT,0)
        
    def non_tir (self) :
        return Vector2D(0,0);
    
    def tir_leger(self) :
      
      if (self.position_balle().y > settings.GAME_HEIGHT/2) :    
        x =0-0.5       
        return Vector2D(angle = x , norm =2)
      elif (self.position_balle().y < settings.GAME_HEIGHT/2) : 
          return Vector2D(angle = 0.5 , norm =2)
      else:
          return Vector2D(angle = 0 , norm =2)
  
  
    def tir_legerD(self) :
      
      if (self.position_balle().y >= settings.GAME_HEIGHT/2) :    
        return Vector2D(angle = 3*(3.12)/2 , norm =2)
      else:
        return Vector2D(angle = 3.12/2 , norm =2)    
    
    def centrerH(self):
        if (self.cornerX() == 1 and self.cornerYH() == 1 ):
                   
            return True
            
    def centrerB(self):

        if (self.cornerX() == 1 and self.cornerYB() == 1 ):
            return True
            
    def aller_centrer(self):
         x = SoccerAction(self.position_balle() - self.position_joueur(), Vector2D(angle = 0.5 , norm =1.5))
         y = SoccerAction(self.position_balle() - self.position_joueur(), Vector2D(angle = (0.5-1) , norm =1.5))
         if (self.position_balle().y > settings.GAME_HEIGHT/2):
               return x
         else:
               return y
          
        
    def tirer_centreH(self):
     
     return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D((settings.GAME_WIDTH*2) /3,settings.GAME_HEIGHT/2)-self.position_joueur())         
            
            
    def tirer_centreB(self):
     
     return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D(-settings.GAME_WIDTH/2,settings.GAME_HEIGHT))            
    
#    def Aller_centre(self):
#        if (self.cornerX and self.cornerY == 1 ):
#            return        
    def tirer_vers(self, c):        
        return SoccerAction( self.position_balle()-self.position_joueur() ,c - self.position_joueur())
        
    def aller_vers(self, c):        
        return SoccerAction( c - self.position_joueur() ,self.non_tir())
        
        
    def position_but_adv(self):
        return (Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2))
      
    def degage(self):
        return Vector2D(settings.GAME_HEIGHT,20)

    def degage_alea(self):
        return Vector2D(settings.GAME_HEIGHT,random.randrange(settings.GAME_HEIGHT/3,(2*settings.GAME_HEIGHT)/3))

    def marquer(self):
        return SoccerAction(self.position_balle() - self.position_joueur() , self.tirer())
        
    def conserver(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.tir_leger())
        
    def conserver2(self):
        return SoccerAction(self.position_balle()-self.position_joueur() , self.tir_legerD())
    
    def degager(self):
        return SoccerAction(self.position_balle() - self.position_joueur(),self.degage_alea())
        
    def positionG(self):
        return SoccerAction((Vector2D(2,settings.GAME_HEIGHT/2))-self.position_joueur(), self.degage())
    
    def positionGH(self):
        return SoccerAction((Vector2D(2,settings.GAME_HEIGHT/2)+5)-self.position_joueur(), self.degage())
     
    def positionGB(self):
        return SoccerAction((Vector2D(2,settings.GAME_HEIGHT/2)-5)-self.position_joueur(), self.degage())
        
    def positionDC(self):
        return SoccerAction((Vector2D(20,settings.GAME_HEIGHT/2))-self.position_joueur(), self.tirer())
    
    def defendre (self):
        return SoccerAction(self.position_balle() - self.position_joueur(),Vector2D(settings.GAME_HEIGHT,0))
    
    def avant_centre(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH*4) /5,settings.GAME_HEIGHT/2)-self.position_joueur(),self.non_tir())

    def millieu(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH) /3,settings.GAME_HEIGHT/2)-self.position_joueur(),self.non_tir())


    def zone_cage(self):
        
        if self.position_balle().y>= (settings.GAME_HEIGHT /2)-5 and self.position_balle().y<= (settings.GAME_HEIGHT /2)+5 :
            return 1
        else:
            return 0
            
    def zone_def(self):
        if self.position_balle().y>= (settings.GAME_HEIGHT /3) and self.position_balle().y<= 2*(settings.GAME_HEIGHT /3) :
            return 1
        else:
            return 0

    
    def suivre_jeuG (self):
      return SoccerAction(Vector2D(5,self.position_balle().y)-self.position_joueur(), self.tirer())
    
    def suivre_jeu(self):
        return SoccerAction(Vector2D(settings.GAME_WIDTH /5,self.position_balle().y)-self.position_joueur(), self.tirer())
        
    def suivre_jeuM(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH)/1.8,self.position_balle().y)-self.position_joueur(), self.tirer())   
        
    def suivre_jeuDC(self):
        return SoccerAction(Vector2D((settings.GAME_WIDTH)/10,self.position_balle().y)-self.position_joueur(), self.tirer())    
    
         
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
         if( self.position_balle().x < settings.GAME_WIDTH / 8 ) :
             return 1
         else:
             return 0
    def zone_de_tir(self) :
         if( self.position_balle().x > settings.GAME_WIDTH - 30) :
             return 1         
         else:
             return 0
    def dans_perimetre(self) :
        if (self.position_balle().y > settings.GAME_HEIGHT/3 and self.position_balle().y < (settings.GAME_HEIGHT*2) / 3) :
            return 1
        else:
             return 0
    def tir_but(self):
        return SoccerAction( self.position_balle()-self.position_joueur() , Vector2D(settings.GAME_WIDTH , (settings.GAME_HEIGHT)/2) - self.position_joueur())
        
    def distance_joueur(self,id_team,id_player):
        return self.position_joueur().distance(self.state.player_state(id_team,id_player).position)
        
    def distance_au_joueur(self):

        j = 0
        for (id_team, id_player) in self.state.players :
            if id_team != self.id_team and self.distance_joueur(id_team,id_player) < 30 and (self.state.player_state(id_team, id_player).position.x >= self.position_joueur().x):
                j=j+1
        if j != 0:
            return 1
        else :
            return 0
  
    def dj2(self):
    
        for (id_team, id_player) in self.state.players :
            if id_team != self.id_team and self.distance_joueur(id_team,id_player) < 30 and (self.state.player_state(id_team, id_player).position.x >= self.position_joueur().x):
                
        
              return self.state.player_state(id_team, id_player)
            else :
             return 0
      
    def defendre_Sur(self,v):
        return SoccerAction(self.v - self.position_joueur(),Vector2D(settings.GAME_HEIGHT,0))
        
    def possede_balleAll(self):

        j = 0
        for (id_team, id_player) in self.state.players :
            if id_team == self.id_team and (self.state.player_state(id_team, id_player).position == self.position_balle()):
                j=j+1
        if j != 0:
            return 1
        else :
            return 0