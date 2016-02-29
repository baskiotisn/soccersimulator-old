# -*- coding: utf-8 -*-
from strat import *
team1 = SoccerTeam("lob", [Player("j1", StrategyP())])
team2 = SoccerTeam("lob",[Player("j1",StrategyAT2()),Player("j2",StrategyGT2())])
team4 = SoccerTeam("lob",[Player("j1",StrategyAT2()),Player("j2",StrategyD()),Player("j3",StrategyP()),Player("j4",StrategyGT2())])

#team1 = SoccerTeam("Madrid", [Player("benzema",StrategyPD())])#,Player("cristiano",StrategyDR())])#,Player("bale",Fonceur()),Player("piquet",Fonceur())])
#team1 = SoccerTeam("Madrid", [Player("benzema",StrategyG())])#,Player("cristiano",StrategyDR())])#,Player("bale",Fonceur()),Player("piquet",Fonceur())])
#team2 = SoccerTeam("Barca",[Player("messi",StrategyG())])#,Player("neymar",StrategyT())])#,Player("suarez",Passeur2()),Player("iniesta",Passeur2())])
