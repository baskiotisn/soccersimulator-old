import soccersimulator
from soccersimulator.settings import *
from soccersimulator import SoccerTeam
from soccersimulator import Player
from soccersimulator import BaseStrategy, Vector2D,SoccerAction
from toolbox import *
from decorator import PlayerStateDecorator

class RandomStrategy(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "Random")

     def compute_strategy(self, state, id_team, id_player):
         return SoccerAction(acceleration = Vector2D.create_random(low=-1.,high=1.), shoot = Vector2D.create_random(low=-1.,high=1.))



class FoncerStrategy(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "Foncer")

     def compute_strategy(self, state, id_team, id_player):
         return suivre_ball (state, id_team, id_player)



class MarquerStrategy(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "Marquer")

     def compute_strategy(self, state, id_team, id_player):
         mystate = PlayerStateDecorator( state, id_team, id_player)
    
         if ((PLAYER_RADIUS + BALL_RADIUS) > mystate.distance_ball()):
             #return SoccerAction(acceleration = state.ball.position - state.player_state(id_team, id_player).position, shoot = Vector2D(150 - state.player_state(id_team, id_player).position.x, 45 - state.player_state(id_team, id_player).position.y))
             return suivre_ball(state, id_team, id_player) + shoot (state, id_team, id_player,GAME_WIDTH,45)
         return suivre_ball (state, id_team, id_player) 
    
     

class DribleStrategy(BaseStrategy):  
     def __init__(self):
        BaseStrategy.__init__(self, "Drible")

     def compute_strategy(self, state, id_team, id_player):
         mystate = PlayerStateDecorator( state, id_team, id_player)
         if ((PLAYER_RADIUS + BALL_RADIUS) > mystate.distance_ball()):
             return suivre_ball (state, id_team, id_player) +  shoot (state, id_team, id_player,5,0)
         return  suivre_ball (state, id_team, id_player)   
               


class DefenseStrategy(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "DefenseD")

     def compute_strategy(self, state, id_team, id_player):
        
         mystate = PlayerStateDecorator ( state, id_team, id_player)
         if ((state.ball.position.distance(cage(id_team)) < 50)): #and (state.ball.position.distance(mystate.adv_proche()) < 1)):
             #if (mystate.dist_adv() > 1):
                 #return suivre_ball (state, id_team, id_player)
             return suivre_ball (state, id_team, id_player) +  shoot (state, id_team, id_player,GAME_WIDTH,80)
          
         return SoccerAction(acceleration = cage(id_team) - state.player_state(id_team, id_player).position, shoot = Vector2D(0,0))

class PasseStrategy(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "Passe")
     
     def compute_strategy(self, state, id_team, id_player):
         mystate = PlayerStateDecorator ( state, id_team, id_player)
         if (mystate.demarque() == False):
             return passe (state, id_team, id_player)
         return suivre_ball (state, id_team, id_player)  +  shoot (state, id_team, id_player,GAME_WIDTH,45)
         