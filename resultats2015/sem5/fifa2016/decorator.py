import soccersimulator

from soccersimulator import BaseStrategy, Vector2D,SoccerAction
from soccersimulator.utils import Vector2D, MobileMixin
from soccersimulator.mdpsoccer import SoccerAction, Configuration, SoccerTeam, SoccerState, Player
from soccersimulator.mdpsoccer import SoccerMatch, SoccerEvents, BaseStrategy, SoccerTournament, Score, KeyboardStrategy
from soccersimulator.interfaces import MatchWindow, show
from soccersimulator.settings import *
from strategies import *
from toolbox import *

class PlayerStateDecorator:
    def __init__(self,state,id_team,id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    def position(self):
        return self.state.player_state(self.id_team,self.id_player).position
    def distance_ball(self):
        return self.state.ball.position.distance(self.position())
    def adv_proche (self):
        return Adv_le_plus_proche (self.state, self.id_team, self.id_player)
    def dist_adv (self):
        #return self.position.distance(self.adv_proche())
        return dist_Adv_le_plus_proche (self.state, self.id_team, self.id_player)
    def demarque (self):
        return self.est_demarque(self.state, self.id_team, self.id_player)