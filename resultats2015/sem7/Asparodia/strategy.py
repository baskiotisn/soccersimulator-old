import tools 
from soccersimulator import BaseStrategy
from tools import PlayerStateDeco
from soccersimulator import KeyboardStrategy
from soccersimulator import  Vector2D, SoccerTeam, Player, SoccerAction

 
class MaStrategyFonceur(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Fonceur")
    def compute_strategy(self, state, id_team, id_player):
        Mystate=PlayerStateDeco(state, id_team, id_player)
        return Mystate.fonceur()
        

        
class MaStrategyDefensive(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		Mystate=PlayerStateDeco(state,id_team,id_player)
		return Mystate.defense()

class MaStrategyGoal(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		Mystate=PlayerStateDeco(state,id_team,id_player)
		return Mystate.goal()

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


"""class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict(self.gen_feat(state,id_team,id_player))[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)"""
