import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *
from zone import *


joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)

team1 = SoccerTeam("team1",[joueur6])
test = SoccerTeam("test",[joueur4])
test2 = SoccerTeam("test2",[joueur2])
team2 = SoccerTeam("team2",[joueur2,joueur4])
team4 = SoccerTeam("team4",[joueur2,joueur5,joueur4,joueur1])

#apprentissage supervise
strat = KeyboardStrategy()
strat.add("f",fonceStrat)
strat.add("g",gardien)
strat.add("a",attaque)
strat.add("d",defense)

eleve = Player("eleve",strat)
team_spe = SoccerTeam("team_eleve",[eleve])

#match = SoccerMatch(team1, team_spe)
match = SoccerMatch(test,test2)
soccersimulator.show(match)
