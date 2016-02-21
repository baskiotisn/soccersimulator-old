# -*- coding: utf-8 -*-
from strat import *
team1 = SoccerTeam("lob", [Player("j1", StrategyP())])
team2 = SoccerTeam("lob",[Player("j1",StrategyP()),Player("j2",StrategyR())])
team4 = SoccerTeam("lob",[Player("j1",StrategyP()),Player("j2",StrategyP()),Player("j3",StrategyR()),Player("j4",StrategyR())])

#team1 = SoccerTeam("Madrid", [Player("benzema", StrategyP())])#,Player("cristiano",StrategyG())])#,Player("bale",Fonceur()),Player("piquet",Fonceur())])
#team2 = SoccerTeam("Barca",[Player("messi",StrategyF())])#,Player("neymar",StrategyF())])#,Player("suarez",Passeur2()),Player("iniesta",Passeur2())])
