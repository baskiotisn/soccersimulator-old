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
from strategy import MaStrategyGoal
from strategy import MaStrategyUtilitaire

from tools import PlayerStateDeco
from soccersimulator import KeyboardStrategy

strat = KeyboardStrategy()
strat.add("a",MaStrategyFonceur())
strat.add("z",MaStrategyDefensive())
strat.add("e",MaStrategyCampeur())
strat.add("r",MaStrategyUtilitaire())

joueur1 = Player("Alpha", strat)
joueur2 = Player("Dourou", MaStrategyCampeur())
joueur3=  Player("Kiba", MaStrategyGoal())
joueur4=  Player("Soro", MaStrategyFonceur())
joueur5 = Player("Dadan", MaStrategyDefensive())
joueur6 = Player("Manque d'inspi", MaStrategyUtilitaire())

team1 = SoccerTeam("Equipe 1", [joueur1,joueur3])
team2 = SoccerTeam("Equipe 2", [joueur4,joueur5])
team4 = SoccerTeam("Equipe 4", [joueur6,joueur2,joueur3,joueur5])


match = SoccerMatch(team1, team4)
soccersimulator.show(match)
strat.write("testexp")



