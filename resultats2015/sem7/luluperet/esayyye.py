import soccersimulator, soccersimulator.settings,math,Walter as W
from soccersimulator.settings import *
from soccersimulator import  SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS
settings=soccersimulator.settings


psg= STe("psg",[Player("Thiago Silva",W.all(2))])
marseille= STe("marseille",[Player("Ocampos",W.all2(3))])
match=SM(psg,marseille)
soccersimulator.show(match)
#tournoi=ST(1)
#tournoi.add_team(psg)
#tournoi.add_team(marseille)
#soccersimulator.show(tournoi)

