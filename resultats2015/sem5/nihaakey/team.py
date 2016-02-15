# -*- coding: utf-8 -*-
from strat import *

team1 = SoccerTeam("lob", [Player("j1", StrategyP())])
team2 = SoccerTeam("lob",[Player("j1",StrategyDR()),Player("j2",StrategyR())])
team4 = SoccerTeam("lob",[Player("j1",StrategyA()),Player("j2",StrategyP()),Player("j3",StrategyI()),Player("j4",StrategyR())])

#team1 = SoccerTeam("Madrid", [Player("benzema", StrategyF())])#,Player("cristiano",StrategyDR())])#,Player("bale",Fonceur()),Player("piquet",Fonceur())])
#team2 = SoccerTeam("Barca",[Player("messi",StrategyDR())])#,Player("neymar",StrategyG())])#,Player("suarez",Passeur2()),Player("iniesta",Passeur2())])
