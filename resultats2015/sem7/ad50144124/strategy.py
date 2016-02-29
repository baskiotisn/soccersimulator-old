# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:03:52 2016

@author: 3407585
"""

import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
"""
============================random================================
"""
class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random()-0.5,
                            Vector2D.create_random())
"""
==========================1V1=====================================
"""

class FoncerStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        state=SoccerStateDecorator(state,id_team,id_player)
        return fonceur(state)

class QuickCatchStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"QuickCatch")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if state.ball.vitesse._x==0 and d.norm<1:
            d.scale(0)
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
"""
=========================2V2=======================================
"""                            
class QuickCatchStrategy2v2(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"QuickCatch2v2")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if state.ball.vitesse._x<0.1 and d.norm<0:
            d.scale(0.09)
        #print state.ball.vitesse
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
                            
class QuickFollowStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"QuickFollow")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if d.norm>5 and state.ball.vitesse._x<0.001:
            d+=Vector2D(-50,20)
        elif state.ball.vitesse._x!=0 or state.ball.vitesse._y!=0 :
            v=state.ball.vitesse.norm
            p=0
            while(v>=0.00001):
                p+=v
                v-=v*0.06-(v**2)*0.01
                #print v
            v=state.ball.vitesse.norm
            vb=state.ball.vitesse 
            vb.scale(p/v)
            d+=vb
        elif d.norm<1:
            d.scale(0.09)
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
                            



                            
    