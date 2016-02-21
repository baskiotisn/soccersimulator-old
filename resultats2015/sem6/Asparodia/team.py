from strategy import MaStrategyFonceur
from strategy import MaStrategyDefensive
from strategy import MaStrategyCampeur
from strategy import MaStrategyUtilitaire
from strategy import MaStrategyGoal
from soccersimulator import SoccerTeam, Player
joueur1 = Player("Alpha", MaStrategyFonceur())
joueur2 = Player("Ocho", MaStrategyDefensive())
joueur3 = Player("Kiba", MaStrategyUtilitaire())
joueur4 = Player("Dadan", MaStrategyCampeur())
joueur5 = Player("Durarara", MaStrategyGoal())

team1 = SoccerTeam("Warrior", [joueur1])
team2 = SoccerTeam("Tremblez!", [joueur2,joueur1])
team4 = SoccerTeam("Lel", [joueur5, joueur2, joueur3, joueur4])

