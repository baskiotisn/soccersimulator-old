import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from PlayerDecorator import *
from zone import *
from tools import *

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")
    def compute_strategy(self, state, teamid, player):
        return SoccerAction(Vector2D.create_random(low=-1.,high=1.), Vector2D.create_random(low=-1.,high=1.))

class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"FonceurStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state, teamid, player)
        return fonceur(etat)
        
class MilieuStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"MilieuStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state, teamid, player)
        return milieu(etat)
        
    
class StratStateless(BaseStrategy):
    def __init__(self,decideur):
        BaseStrategy.__init__(self,decideur.__name__)
        self.decideur = decideur
    def compute_strategy(self,state,idt,idp):
        return  self.decideur(PlayerDecorator(state,idt,idp)) 


class GoalStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"GoalStrategy")
    def compute_strategy(self, state, teamid,player):
        etat = PlayerDecorator(state,teamid,player)
        return goal(etat)



joueur1 = Player("Joueur 1", FonceurStrategy())
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur2 = Player("Joueur 2", GoalStrategy())
#team1 = SoccerTeam("team1",[joueur1])
#team2 = SoccerTeam("team2",[joueur5])
team1 = SoccerTeam("team1",[joueur1,joueur2,joueur3,joueur3])
team2 = SoccerTeam("team2",[joueur1,joueur2,joueur3,joueur3])
#match = SoccerMatch(team1, team2)
#soccersimulator.show(match)
