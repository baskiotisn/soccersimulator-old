from Strategies import*
from soccersimulator import SoccerTeam, Player

#### Mes tests
Priya_1a = SoccerTeam("Priya_1a",[Player("f1",FonceurStrat)])
Priya_1b =SoccerTeam("Priya_1b",[Player("GARDIEN",Gard_shoot_but)])

Priya_2a = SoccerTeam("Priya_2a",[Player("1DEFa",DefStrat),Player("GARDIENa",Gard_shoot_but)])
Priya_2b =SoccerTeam("Priya_2b",[Player("1ATTb",FonceurStrat),Player("GARDIENb",Gard_shoot_alea)])

Priya_4a = SoccerTeam("Priya_4a",[Player("MILIEU",milieustrat),Player("GARDIENa",Gard_shoot_but),Player("2ATTa",FonceurStrat),Player("1DEFa",DefStrat)])
Priya_4b =SoccerTeam("Priya_4b",[Player("1ATTb",FonceurStrat),Player("GARDIENb",Gard_shoot_but),Player("2ATTb",FonceurStrat),Player("1DEFb",DefStrat)])


### Pour le tournoi
team1 = SoccerTeam("team1",[Player("f1",FonceurStrat)])
team2 = SoccerTeam("team2",[Player("ATT1",FonceurStrat),Player("GARD",Gard_shoot_but)])
team4 = SoccerTeam("team4",[Player("ATT1",FonceurStrat),Player("gk2",Gard_shoot_but),Player("ATT2",FonceurStrat),Player("DEF1",DefStrat)])
