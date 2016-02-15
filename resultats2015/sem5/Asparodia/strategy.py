import tools 
from soccersimulator import BaseStrategy
from tools import PlayerStateDeco

 
class MaStrategyFonceur(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Fonceur")
    def compute_strategy(self, state, id_team, id_player):
        Mystate=PlayerStateDeco(state, id_team, id_player)
        return Mystate.suivre_balle()+ Mystate.shoot()
        

        
class MaStrategyDefensive(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		Mystate=PlayerStateDeco(state,id_team,id_player)
		return Mystate.defense()

class MaStrategyCampeur(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Fonceur")
    def compute_strategy(self, state, id_team, id_player):
        Mystate=PlayerStateDeco(state, id_team, id_player)
        return Mystate.campe()

class MaStrategyUtilitaire(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Fonceur")
    def compute_strategy(self, state, id_team, id_player):
        Mystate=PlayerStateDeco(state, id_team, id_player)
        return Mystate.utilitaire()
