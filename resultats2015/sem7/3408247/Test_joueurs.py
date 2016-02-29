# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:44:42 2016

@author: 3408247
"""

import soccersimulator
from soccersimulator.settings import  *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament

import Strategies

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        
        if id_team==1:
            position_milieu_but=Vector2D(x=150.,y=45.)
            
        if id_team==2:
            position_milieu_but=Vector2D(x=0.,y=45.)
            
        vector_acc=state.ball.position-state.player_state(id_team,id_player).position
        
        if (state.ball.position.distance(state.player_state(id_team,id_player).position)<BALL_RADIUS+PLAYER_RADIUS):
            vector_shoot=position_milieu_but-state.ball.position
        else:
            vector_shoot=Vector2D()
        
        return SoccerAction(vector_acc,vector_shoot)
    
    
team1= SoccerTeam("team1",[(Player("t1j1",RandomStrategy())),(Player("t1j2",RandomStrategy()))])
team2= SoccerTeam("team2",[Player("t2j1",RandomStrategy()),(Player("t2j2",RandomStrategy()))])
team3= SoccerTeam("team3",[Player("t3j1",RandomStrategy())])
match=SoccerMatch(team1,team2)

soccersimulator.show(match)
tournoi=SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)
tournoi.add_team(team3)
soccersimulator.show(tournoi)
