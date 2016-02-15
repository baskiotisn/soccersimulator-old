from strategy import MaStrategyFonceur
from strategy import MaStrategyDefensive
from strategy import MaStrategyCampeur
from strategy import MaStrategyUtilitaire
from soccersimulator import SoccerTeam, Player
joueur1 = Player("Alpha", MaStrategyFonceur())
joueur2 = Player("Ocho", MaStrategyDefensive())
joueur3 = Player("Kiba", MaStrategyUtilitaire())
joueur4 = Player("Dadan", MaStrategyCampeur())
joueur5 = Player("Durarara", MaStrategyUtilitaire())

team1 = SoccerTeam("Equipe 1", [joueur1])
team2 = SoccerTeam("Equipe 2", [joueur3,joueur4])
team4 = SoccerTeam("Equipe 4", [joueur2, joueur3, joueur4, joueur5])

