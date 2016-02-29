# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:23:06 2016

@author: 3200404
"""


from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
from soccersimulator import Vector2D
from soccersimulator import settings
from tools import *
from PlayerStrat import *




class Strat(BaseStrategy):
    def __init__(self,comportement,name):
        BaseStrategy.__init__(self,name)
        self.comportement = comportement
    def compute_strategy(self, state, id_team, id_player):
        s_miroir = state
        if id_team==1 :
            Mystate = PlayerDecorator(s_miroir,id_team , id_player)
            return self.comportement(Mystate)
        else :
            s_miroir = miroir_st(state)
            Mystate = PlayerDecorator(s_miroir,id_team , id_player)
            return miroir_sa(self.comportement(Mystate))
    
    
keytest = KeyboardStrategy(fn = "mon_fichier")

goalG = Strat(goal, "goal")
attaqueG = Strat(scoreG,"attaquant")
defenseG = Strat(defence,"defenseur")
lateralG = Strat(lateral,"lateral")
pointe = Strat(fullStrike,"pointe")
millieu = Strat(millieu,"millieu")
central = Strat(Dcentral,"dc")

keytest.add("g",goalG)
keytest.add("d",defenseG)
keytest.add("a",attaqueG)
keytest.add("m",millieu)
keytest.add("l",lateralG)
class Goal(BaseStrategy):
  
  def __init__(self):
      BaseStrategy.__init__(self, "Random")
 
  def compute_strategy(self,state,id_team,id_player):
      MyState = PlayerDecorator(state ,id_team , id_player) 
      p = state.player_state(id_team,id_player)
      
      
      return goal(MyState,p)
  
        


class GoalG(BaseStrategy):
  
  def __init__(self):
      BaseStrategy.__init__(self, "Random")
 
  def compute_strategy(self,state,id_team,id_player):
   p = state.player_state(id_team,id_player) 
  
   if (state.ball.position.x <= 20 and state.ball.position.y > 35 and state.ball.position.y < 55):
        return SoccerAction((state.ball.position - p.position),Vector2D(settings.GAME_HEIGHT,0))
   else :
        return SoccerAction(Vector2D(10,settings.GAME_HEIGHT/2)-p.position, Vector2D(settings.GAME_HEIGHT,0))
   
   


class Defence(BaseStrategy):
   def __init__(self):
      BaseStrategy.__init__(self, "Random")
   def compute_strategy(self,state,id_team,id_player):
     p = state.player_state(id_team,id_player) 
     MyState = PlayerDecorator(state ,id_team , id_player) 
       
       
     if (MyState.distanceAll() < 10) :
         return SoccerAction(Vector2D(settings.GAME_WIDTH -70,state.ball.position.y)-p.position, Vector2D(0,0))
   
     if (MyState.position_balle()> 75):
         return SoccerAction((state.ball.position - p.position),Vector2D(-(settings.GAME_HEIGHT),0))
  
     else :
         return SoccerAction(Vector2D(settings.GAME_WIDTH -70,state.ball.position.y)-p.position, Vector2D(0,0))
         


class Defence2(BaseStrategy):
   def __init__(self):
     
     BaseStrategy.__init__(self, "Random")
   
   def compute_strategy(self,state,id_team,id_player):
   
      p = state.player_state(id_team,id_player) 
    
      if (state.ball.position.x < 75):
        return SoccerAction((state.ball.position - p.position),Vector2D((settings.GAME_HEIGHT),0))
      else:
        return SoccerAction(Vector2D(70,state.ball.position.y)-p.position, Vector2D(0,0))        
   


class ScoreG(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     
     def compute_strategy(self,state,id_team,id_player): 
        MyState = PlayerDecorator(state ,id_team , id_player) 
        p = state.player_state(id_team,id_player)
       
        return scoreG(MyState,p)
  
       
       
class Score2(BaseStrategy):
     def __init__(self):
      BaseStrategy.__init__(self, "Random")
     def compute_strategy(self,state,id_team,id_player):
       p = state.player_state(id_team,id_player)   
       return SoccerAction(state.ball.position - p.position,Vector2D(-(settings.GAME_HEIGHT),0))
