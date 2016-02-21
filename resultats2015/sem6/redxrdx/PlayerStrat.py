# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 17:05:52 2016

@author: 3200404
"""
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import Vector2D
from soccersimulator import settings
from tools import *


def goal(MyState):   
     
 
   if MyState.sortieGardien() == 1 and MyState.dans_perimetre() == 1 :
   
     
      return MyState.degager()
   
   elif (MyState.zone_cage() == 1):
        return MyState.suivre_jeuG()   
   
   else:
  
      return MyState.positionG()
       
      
      
def scoreG(MyState):
   
    if (MyState.dans_perimetre() == 1 and MyState.zone_de_tir() == 1) :
       return MyState.marquer()
       
    
    else :
       return MyState.conserver()         
    
    
    
    
def defence(MyState):

    if (MyState.possede_balle() == 1):
        return MyState.marquer()    
    
    if (MyState.balle_chez_adv()) :
        return  MyState.suivre_jeu()
    else :
        return MyState.defendre()



def fullStrike(MyState) :
  
 
 if MyState.balle_chez_adv() :

   if (MyState.dans_perimetre() == 1 or MyState.position_balle().x > settings.GAME_WIDTH - 30):
        return MyState.marquer()  
   else :
        return MyState.avant_centre()    
 elif(MyState.balle_chez_nous()):
     
     return MyState.avant_centre()      
        
def lateral(MyState) :
  if (MyState.balle_chez_adv()) :    
    if MyState.centrerH() :
       
        return MyState.tirer_centreH()
   
   
    if MyState.centrerB() : 
        
        return MyState.tirer_centreB()
    else:
        return MyState.aller_centrer()        
        
  else:
     if (MyState.possede_balle == 1):
        return MyState.conserver() 
     else :
           return  MyState.suivre_jeu()