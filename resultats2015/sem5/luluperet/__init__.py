import soccersimulator, soccersimulator.settings,math,AllStrategies as AllS, As
from soccersimulator.settings import *
from soccersimulator import  SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS
settings=soccersimulator.settings



team1= STe("psg",[Player("L1a1ss",AllS.all(2))])
team2= STe("psg",[Player("L1a1ss",AllS.all(2)),Player("Ibra",AllS.all(3))])
team4=STe("mars",[Player("L1a1ss",AllS.all(2)),Player("Ibra",AllS.all(1)),Player("Ibra",AllS.all(3)),Player("L1a1s",AllS.all(2))])
