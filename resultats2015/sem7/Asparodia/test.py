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
import soccersimulator
from tools import PlayerStateDeco
from soccersimulator import KeyboardStrategy

strat = KeyboardStrategy()
strat.add("a",MaStrategyFonceur())
strat.add("z",MaStrategyDefensive())
strat.add("e",MaStrategyUtilitaire())
strat.add("r",MaStrategyGoal())

joueur1 = Player("Alpha", strat)
joueur2 = Player("Dourou", MaStrategyCampeur())
joueur3=  Player("Kiba", MaStrategyGoal())
joueur4=  Player("Soro", MaStrategyFonceur())
joueur5 = Player("Dadan", MaStrategyDefensive())
joueur6 = Player("Manque d'inspi", MaStrategyUtilitaire())

team1 = SoccerTeam("Equipe 1", [joueur1,joueur3])
team2 = SoccerTeam("Equipe 2", [joueur5,joueur3])
team3 = SoccerTeam("Equipe 3", [joueur1,joueur2,joueur3,joueur5]) 
team4 = SoccerTeam("Equipe 4", [joueur6,joueur2,joueur3,joueur5])


match = SoccerMatch(team3, team4)
soccersimulator.show(match)
strat.write("test4v4_7.exp")



