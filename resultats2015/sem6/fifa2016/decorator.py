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
        
    def coop_proche (self, state):
       for (self.id_team, id_player) in state.players :
            if (self.position().distance(state.player_state(self.id_team , id_player).position) < 10): 
                return True
            else :
                return False
                
    def coop_pos (self, state):
       for (self.id_team, id_player) in state.players :
            if (self.position().distance(state.player_state(self.id_team , id_player).position) < 10): 
                return state.player_state(self.id_team , id_player).position
           
                
    def danger (self, state):
        for (id_team, id_player) in state.players :
            if (self.position().distance(state.player_state(id_team , id_player).position) < 5) :
                return True
            else :
                return False
    
    def aller_a (self, v):
        return SoccerAction ( v - self.position(), Vector2D())   
    
    def shoot_vers (self, v):
        vect = v - self.position()
        return SoccerAction (Vector2D(), miroir(self.id_team, vect)) 
        
    def passe (self, state):
       if (self.coop_proche(state)):
           ply = self.coop_pos(state)
           return shoot_vers (ply)