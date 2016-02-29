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
        
    def player_pos(self,idteam,idplayer):
		return self.state.player_state(idteam,idplayer).position    
  
    def distance_ball(self):
        return self.state.ball.position.distance(self.position())
        
    def coop_proche (self, state):
       for (self.id_team, id_player) in state.players :
            if (self.position().distance(state.player_state(self.id_team , id_player).position) < 10): 
                return True
            else :
                return False
                
    def coop_pos (self, state):
       dist = 4000
       for (self.id_team, id_player) in state.players :
           if (self.position().distance(state.player_state(self.id_team , id_player).position) < dist): 
                dist = self.position().distance(state.player_state(self.id_team , id_player).position)
                coop = state.player_state(self.id_team , id_player).position
           return coop
                
    def get_coop (self, state):
        return sorted([ (self.position().distance(self.player(self.id_team,id_player)),id_team,id_player) for (id_team, id_player) in self.state.players if id_team == self.id_team])
                
    def danger (self, state):
        for (id_team, id_player) in state.players :
            if (self.position().distance(state.player_state(id_team , id_player).position) < 5) :
                return True
            else :
                return False
    
    def aller_a (self, v):
        return SoccerAction ( v - self.position(), Vector2D())   
    
    def shoot_vers (self, v):
        return SoccerAction (Vector2D(), v - self.position()) 
        
    def passe (self, state):
       if (self.danger(self, state)):
           ply = self.coop_pos(state)
           return shoot_vers (ply)
           
    def mes_buts (self):
        if (self.id_team == 2):
         return Vector2D(145,45)
        if (self.id_team ==1):
         return Vector2D(5,45)
         
    def adv_buts (self):
        if (self.id_team == 1):
         return Vector2D(145,45)
        if (self.id_team == 2):
         return Vector2D(5,45)