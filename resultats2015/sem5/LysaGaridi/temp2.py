# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import soccersimulator, soccersimulator.settings
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, SoccerMatch, SoccerTeam, Player, SoccerTournament, settings, Player
import math





"""
class MaStrategy(AbstractStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction(Vector2D.create_random(),Vector2D.create_random())
        
team1 = SoccerTeam("team1", [Player("t1j1", MaStrategy())])
team2 = SoccerTeam("team2", [Player("t2j1", MaStrategy())])
team3 = SoccerTeam("team3", [Player("t3j1", MaStrategy())])
match = SoccerMatch(team1, team2)
tournoi = SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)
tournoi.add_team(team3)
soccersimulator.show(tournoi)
"""



class MaStrategy1Goal(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        ppos = state.player_state(id_team, id_player).position
        bpos = state.ball.position
        pset = settings.PLAYER_RADIUS
        bset = settings.BALL_RADIUS
        butset = Vector2D(0,settings.GAME_HEIGHT/2.)
        """gset = settings.GAME_GOAL_HEIGHT"""
        action = SoccerAction(butset-ppos,Vector2D())
        if ppos.distance(bpos) < 50 :
            action += SoccerAction(Vector2D(), Vector2D(-10,0))
        return action

class MaStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        ppos = state.player_state(id_team, id_player).position
        bpos = state.ball.position
        pset = settings.PLAYER_RADIUS
        bset = settings.BALL_RADIUS
        """gset = settings.GAME_GOAL_HEIGHT"""
        butset = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
        action = SoccerAction(acceleration = bpos-ppos)
        if ppos.distance(bpos) < (pset+bset) :
            action += SoccerAction(shoot = butset-ppos)
        return action
        

class MaStrategy2Goal(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        ppos = state.player_state(id_team, id_player).position
        bpos = state.ball.position
        pset = settings.PLAYER_RADIUS
        bset = settings.BALL_RADIUS
        butset = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        """gset = settings.GAME_GOAL_HEIGHT"""
        action = SoccerAction(butset-ppos,Vector2D())
        if ppos.distance(bpos) < 50 :
            action += SoccerAction(Vector2D(), Vector2D(-10,0))
        return action
        

class MaStrategy2(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        ppos = state.player_state(id_team, id_player).position
        bpos = state.ball.position
        pset = settings.PLAYER_RADIUS
        bset = settings.BALL_RADIUS
        """gset = settings.GAME_GOAL_HEIGHT"""
        butset = Vector2D(0, settings.GAME_HEIGHT/2)
        action = SoccerAction(acceleration = bpos-ppos)
        if ppos.distance(bpos) < (pset+bset) :
            action += SoccerAction(shoot = butset-ppos)
        return action
        

        
"""class MaStrategy3(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        ppos = state.player_state(id_team, id_player).position
        bpos = state.ball.position
        pset = settings.PLAYER_RADIUS
        bset = settings.BALL_RADIUS
        gset = settings.GAME_GOAL_HEIGHT
        action = SoccerAction(acceleration = bpos-ppos)
        if ppos.distance(bpos) < (pset+bset) :
            action += SoccerAction(shoot = gset-pset)
        return action """

        
joueur11 = Player("t1j1", MaStrategy())
joueur12 = Player("t1j2", MaStrategy1Goal())
joueur13 = Player("t1j3", MaStrategy())
joueur21 = Player("t2j1", MaStrategy2())
joueur22 = Player("t2j2", MaStrategy2Goal())
joueur23 = Player("t2j3", MaStrategy2())
team1 = SoccerTeam("team1", [joueur11, joueur12])
team2 = SoccerTeam("team2", [joueur21, joueur22])
match = SoccerMatch(team1, team2, 1000)
soccersimulator.show(match)
