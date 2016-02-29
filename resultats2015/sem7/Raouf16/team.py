import soccersimulator
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament
from Strat import attaquant, defenseur_central, defenseur_gauche, defenseur_droit, milieu, milieu_defensif, attaquant_pointe


team1 = SoccerTeam ("DZPOWER",[Player("Messi",attaquant)])

team2 = SoccerTeam ("DZPOWER",[Player("Raouf",attaquant), Player("Yacine",defenseur_central)])

team4 = SoccerTeam ("DZPOWER",[Player("Raouf",attaquant_pointe), Player("Yacine",milieu_defensif), Player("Raouf JR",milieu), Player("Yacine JR",defenseur_central)])


