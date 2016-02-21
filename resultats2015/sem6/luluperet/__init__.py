import soccersimulator, soccersimulator.settings,math,Walter as W
from soccersimulator.settings import *
from soccersimulator import  SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS
settings=soccersimulator.settings



team1= STe("psg",[Player("Thiago Silva",W.all(2))])
team2= STe("psg",[Player("Thiago Silva",W.all(2)),Player("Ibra",W.all(3))])
team4=STe("mars",[Player("Thiago Silva",W.all(2)),Player("Ibra",W.all(1)),Player("Cavani",W.all(3)),Player("Thiago Silva",W.all(2))])
