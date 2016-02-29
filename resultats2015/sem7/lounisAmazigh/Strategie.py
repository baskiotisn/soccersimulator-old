#import soccersimulator
#import random
#from soccersimulator import SoccerTeam, SoccerMatch
from  soccersimulator import settings
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
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
    
keytest = KeyboardStrategy(fn = "fichier")
    


goal_strat = Strat(goal , "1")
attaque_Strategy = Strat(attaque_pointe,"attaquant")
defense_Strategy = Strat(defenseur1,"def")
milieu = Strat(milieu_centre , "mil")      
milieu_deffa = Strat(milieu_def , "milOf")
test = Strat(test1, "test")
P1_fonceur = Strat(attaquant1 , "att")
T2_All = Strat(player_go , "tout")
attaquant_gauche = Strat(attaque_gauche , "7")
att_def_droit = Strat(marcelo , "2")
def_gauche = Strat(deff_gauche , "3")

keytest.add("b" , defense_Strategy  )
keytest.add("a" , attaque_Strategy  )           
keytest.add("z" , milieu )  
keytest.add("g" , goal_strat  )     

print "keytest"
print(keytest)   
