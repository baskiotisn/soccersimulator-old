# -*-coding: utf8 -*
import soccersimulator
from soccersimulator.settings import *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
import strategy
from strategy import Mystate


class AllStrategy(BaseStrategy):
    def __init__(self,comportement):
        BaseStrategy.__init__(self,comportement.__name__)
        self.comportement = comportement

    def compute_strategy(self,state, id_team,id_player):
        mystate = Mystate(strategy.miroir_state(state) if id_team != 1 else state,id_team,id_player)
        res = self.comportement(mystate)
        if id_team == 2:
            res = strategy.miroir_socac(res)
        return res



passeur = AllStrategy(strategy.essai)
z = AllStrategy(strategy.rien)


player_team1 = AllStrategy(strategy.player_team1)
player_team2 = AllStrategy(strategy.player_team2)
player_team41 = AllStrategy(strategy.player_team41)
player_team42 = AllStrategy(strategy.player_team42)
attaquant = AllStrategy(strategy.fonceur_shooteur)
attaquante = AllStrategy(strategy.shooteur_ball_smart)

defenseur  = AllStrategy(strategy.defenseur)

gardien = AllStrategy(strategy.gardien)
gardien_team4 = AllStrategy(strategy.gardien_team4)
