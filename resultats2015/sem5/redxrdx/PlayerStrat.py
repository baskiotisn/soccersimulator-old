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
   
   else:
  
      return MyState.positionG()
       
      
      
def scoreG(MyState):
   
      

             return MyState.marquer()
    
    
    
    
def defence(MyState):


    if (MyState.balle_chez_adv()) :
        return  MyState.suivre_jeu()
    else :
        return MyState.defendre()

        