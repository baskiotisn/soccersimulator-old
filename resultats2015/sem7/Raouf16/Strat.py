from  soccersimulator import settings
from soccersimulator import BaseStrategy, SoccerAction
from Tools import *


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


attaquant = Strat(attaquant_fonceur, "R")
attaquant_pointe = Strat(attaquant_pointe, "X")
defenseur_central = Strat(defenseur_central, "Y")
defenseur_gauche = Strat(defenseur_gauche, "M")
defenseur_droit = Strat(defenseur_droit, "B")
milieu = Strat(milieu, "S")
milieu_defensif = Strat(milieu_defensif, "F")
