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
dribleur = AllStrategy(strategy.dribleur)

player_team1 = AllStrategy(strategy.player_team1)
player_team2 = AllStrategy(strategy.player_team2)
player_team41 = AllStrategy(strategy.player_team41)
player_team42 = AllStrategy(strategy.player_team42)
attaquant = AllStrategy(strategy.fonceur_shooteur)


defenseur  = AllStrategy(strategy.defenseur)

gardien = AllStrategy(strategy.gardien)
gardien_team4 = AllStrategy(strategy.gardien_team4)


######################################################################################################
#                      Ensemble de strategies générales pour la KeyboardStrategy
######################################################################################################
fonceur_shooteur = AllStrategy(strategy.fonceur_shooteur)
buteur = AllStrategy(strategy.shooteur_ball_smart)
runv_goal = AllStrategy(strategy.run_ball_avant_normalize)
runv_goal_arr = AllStrategy(strategy.run_ball_arriere_normalize)
