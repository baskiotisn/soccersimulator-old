import soccersimulator, soccersimulator.settings,math,AllStrategies as AllS
from soccersimulator.settings import *
from soccersimulator import  SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS
settings=soccersimulator.settings


psg= STe("psg",[Player("Ibra",AllS.all(1)),Player("Ibra",AllS.all(3))])
marseille= STe("marseille",[Player("L1a1ss",AllS.all(2)),Player("L1a1ss",AllS.all(3))])
match=SM(psg,marseille)
soccersimulator.show(match)
#tournoi=ST(1)
#tournoi.add_team(psg)
#tournoi.add_team(marseille)
#soccersimulator.show(tournoi)

