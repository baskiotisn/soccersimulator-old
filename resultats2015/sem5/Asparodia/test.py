import random
import math
import soccersimulator,soccersimulator.settings
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator.settings import *
from strategy import MaStrategyFonceur
from strategy import MaStrategyDefensive
from strategy import MaStrategyCampeur
from strategy import MaStrategyUtilitaire
from tools import PlayerStateDeco


joueur1 = Player("Alpha", MaStrategyUtilitaire())
joueur2 = Player("Dourou", MaStrategyCampeur())
joueur3=  Player("Kiba", MaStrategyDefensive())
joueur4=  Player("Soro", MaStrategyFonceur())
joueur5 = Player("Dadan", MaStrategyUtilitaire())

team1 = SoccerTeam("Equipe 1", [joueur1, joueur4])
team2 = SoccerTeam("Equipe 2", [joueur3, joueur4])
team4 = SoccerTeam("Equipe 4", [joueur1,joueur2,joueur3,joueur5])


match = SoccerMatch(team1, team4)
soccersimulator.show(match)
