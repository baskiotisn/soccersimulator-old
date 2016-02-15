import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from projet import *
from PlayerDecorator import *

joueur1 = Player("Joueur 1", FonceurStrategy())
joueur2 = Player("Joueur 2", GoalStrategy())
joueur3 = Player("Joueur 3", MilieuStrategy())


team1 = SoccerTeam("team1",[joueur3,joueur2])
team2 = SoccerTeam("team2",[joueur2,joueur1])
team4 = SoccerTeam("team4",[joueur1,joueur2,joueur3,joueur3])

match = SoccerMatch(team2, team1)
soccersimulator.show(match)
