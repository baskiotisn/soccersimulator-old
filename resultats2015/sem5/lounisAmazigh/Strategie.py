#import soccersimulator
#import random
#from soccersimulator import SoccerTeam, SoccerMatch
from  soccersimulator import settings
from soccersimulator import BaseStrategy, SoccerAction 
from Tools import *
from Player_strat import *

class Strat(BaseStrategy):
    def __init__(self,comportement,name):
        BaseStrategy.__init__(self,name)
        self.comportement = comportement
    def compute_strategy(self, state, id_team, id_player):
        s_miroir = state
        if id_team==1 :
            Mystate = PlayerStateDecorator(s_miroir,id_team , id_player)
            return self.comportement(Mystate)
        else :
            s_miroir = miroir_st(state)
            Mystate = PlayerStateDecorator(s_miroir,id_team , id_player)
            return miroir_sa(self.comportement(Mystate))
    
    
goal_strat = Strat(goal , "1")
attaque_Strategy = Strat(attaque_pointe,"attaquant")
defense_Strategy = Strat(defenseur1,"def")
milieu = Strat(milieu_centre , "mil")      
milieu_attaquant = Strat(milieu_att , "milOf")
test = Strat(test1, "test")
P1_fonceur = Strat(attaquant1 , "att")
T2_All = Strat(player_go , "tout")
"""       
class Test(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "test")
        
    def compute_strategy(self , state , id_team , id_player ):
        Mystate = PlayerStateDecorator(state , id_team , id_player)
        
        if Mystate.can_shoot() == True : 
            return  Mystate.shoot_to_cage_t2()
        else:
            return  Mystate.suivre_bal() 
     
        return Mystate.shoot_to_cage_t1() + Mystate.suivre_bal()

        return milieu_centre(Mystate)
        


class team2_strat(BaseStrategy):
     def __init__(self):
        BaseStrategy.__init__(self, "MIL-OF")
        
     def compute_strategy(self , state , id_team , id_player ):
        Mystate = PlayerStateDecorator(state , id_team , id_player) 
        
        return milieu_att(Mystate)"""
        




























                    
"""class MaStrategy(BaseStrategy):
      def __init__(self):
         BaseStrategy.__init__(self, "Basic")
         
      def compute_strategy(self, state, id_team, id_player):

          bal = state.ball.position
          p = state.player_state(id_team, id_player) 
         
          if  (p.position.distance(bal) < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
              return shoot_bal(state , id_team ,id_player)
          else : 
              return suivre_bal(state , id_team, id_player)"""
              
              
              
              
              
              
              
              
              
              
