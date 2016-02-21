from projet import *

joueur1 = Player("Joueur 1", fonceStrat)
joueur2 = Player("Joueur 2", gardien)
joueur3 = Player("Joueur 3", MilieuStrategy())
joueur4 = Player("Joueur 4", attaque)
joueur5 = Player("Joueur 5", defense)
joueur6 = Player("Joueur 6", j_solo)

team1 = SoccerTeam("team2",[joueur6])
team2 = SoccerTeam("team1",[joueur2,joueur4])
team4 = SoccerTeam("team4",[joueur2,joueur5,joueur4,joueur1])
