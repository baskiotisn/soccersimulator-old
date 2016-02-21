import soccersimulator


from soccersimulator.utils import Vector2D, MobileMixin
from soccersimulator.mdpsoccer import SoccerAction, Configuration, SoccerTeam, SoccerState, Player
from soccersimulator.mdpsoccer import SoccerMatch, SoccerEvents, BaseStrategy, SoccerTournament, Score, KeyboardStrategy
from soccersimulator.interfaces import MatchWindow, show
from soccersimulator.settings import *
from strategies import *

def dist_Adv_le_plus_proche (state, id_team, id_player):
   dist = 4000
   for player in [ (it, ip) for (it, ip) in state.players if it != id_team] :
       if (dist >  state.player_state(id_team, id_player).position.distance(state.player(it,ip).position)):
          dist =  state.player_state(id_team, id_player).position.distance(state.player(it,ip).position)
          #adv = state.player(it, ip).position
   return dist
   
def Adv_le_plus_proche (state, id_team, id_player):
   dist = 4000
   for player in [ (it, ip) for (it, ip) in state.players if it != id_team] :
       if (dist >  state.player_state(id_team, id_player).position.distance(state.player(it,ip).position)):
          dist =  state.player_state(id_team, id_player).position.distance(state.player(it,ip).position)
          adv = state.player(it, ip).position
   return adv 

def suivre_ball (state, id_team, id_player):
    return SoccerAction (acceleration = state.ball.position - state.player_state(id_team, id_player).position, shoot = Vector2D(0,0))
 
def cage (id_team):
    
     if (id_team == 2):
         return Vector2D(145,45)
     if (id_team ==1):
         return Vector2D(5,45)


def miroir (id_team, v):
   if (id_team == 2):
      return Vector2D(-1*v.x , v.y)  
   return Vector2D(v.x , v.y)
    
def shoot (state, id_team, id_player, X, Y):
    if (id_team == 2):
        return SoccerAction (acceleration = Vector2D(0,0), shoot = Vector2D(-(X - state.player_state(id_team, id_player).position.x), Y - state.player_state(id_team, id_player).position.y))
    if (id_team == 1):
        return SoccerAction (acceleration = Vector2D(0,0), shoot = Vector2D( X - state.player_state(id_team, id_player).position.x, Y - state.player_state(id_team, id_player).position.y))
#def shoot (state, id_team, id_player):
    #return SoccerAction (acceleration = Vector2D(0,0), shoot = GD(id_team,Vector2D(GAME_WIDTH,0))
def est_demarque (state, id_team, id_player):
    
   if ( dist_Adv_le_plus_proche (state, id_team, id_player) < 10):
           return False 
   return True
    
def passe(state, id_team, id_player) :
    
    for palyer in [ (it, ip) for (it, ip) in state.players if it == id_team] :
        if (est_demarque(state, it, ip)):
            return SoccerAction (acceleration = Vector2D(0,0), shoot = Vector2D(state.palyer(it, ip).position.x - state.player_state(id_team, id_player).position.x, state.palyer(it, ip).position.y - state.player_state(id_team, id_player).position.y))
    return SoccerAction()
