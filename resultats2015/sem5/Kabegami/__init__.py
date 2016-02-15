from projet import *

joueur1 = Player("Joueur 1", FonceurStrategy())
joueur2 = Player("Joueur 2", GoalStrategy())
joueur3 = Player("Joueur 3", MilieuStrategy())

team1 = SoccerTeam("team1",[joueur1])
team2 = SoccerTeam("team2",[joueur1,joueur2])
team4 = SoccerTeam("team4",[joueur1,joueur2,joueur1,joueur1])
