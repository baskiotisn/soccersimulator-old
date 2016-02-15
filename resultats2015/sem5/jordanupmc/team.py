from Strat import *

team1=SoccerTeam("equipe1",[Player("Bravo",GardienStrategy())])
team11=SoccerTeam("equipe11",[Player("Costa",FonceurStrategy())])

team2=SoccerTeam("equipe2",[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())])
team4=SoccerTeam("equipe4",[Player("t3j1",FonceurStrategy())],[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())])
