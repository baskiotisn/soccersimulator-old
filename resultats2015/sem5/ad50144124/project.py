# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

"""

import soccersimulator,soccersimulator.settings
from decorator import *
from strategy import *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament



"""
============================main===================================
"""
class StateLessStrategy(BaseStrategy):
    def __init__(self, decid):
        BaseStrategy.__init__(self,decid.__name__)
        self.decideur = decid
        self.info = dict()        
    def compute_strategy(self,state,id_team,id_player):
        return self.decideur(SoccerStateDecorator(state,id_team,id_player,self.info))



#team1=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(random))])
#team2=SoccerTeam("team2",[Player("t2j1",StateLessStrategy(Smart1v1))])

team1=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(random)),Player("t1j2",StateLessStrategy(Smart1v1))])
team2=SoccerTeam("team1",[Player("t2j1",StateLessStrategy(Smart2v2)),Player("t2j2",StateLessStrategy(Smart2v2))])

#team1=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(fonceur)),Player("t1j2",StateLessStrategy(fonceur)),Player("t1j3",StateLessStrategy(fonceur)),Player("t1j4",StateLessStrategy(fonceur))])
#team2=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(Smart1v1)),Player("t1j2",StateLessStrategy(Smart1v1)),Player("t1j3",StateLessStrategy(Smart1v1)),Player("t1j4",StateLessStrategy(Smart1v1))])



match=SoccerMatch(team1,team2)
soccersimulator.show(match)

#tournoi = SoccerTournament(1)
#tournoi.add_team(team1)
#tournoi.add_team(team2)

#tournoi.play()
#soccersimulator.show(tournoi)
