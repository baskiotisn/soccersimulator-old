# -*- coding: utf-8 -*-

from soccersimulator import SoccerTeam, Player
from strategies import MaStrategy, MaStrategyGoal



#joueur1 = Player("t1j1", MaStrategy())
#team1 = SoccerTeam("team1", [joueur1])

joueur11 = Player("t11j11", MaStrategy())
team11 = SoccerTeam("team11", [joueur11])


joueur21 = Player("t2j1", MaStrategy())
joueur22 = Player("t2j2", MaStrategyGoal())
team2 = SoccerTeam("team2", [joueur21, joueur22])


team1 = team2
