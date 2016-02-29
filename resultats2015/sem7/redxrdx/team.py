# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:29:33 2016

@author: 3200404
"""

 

from strategie import *
from soccersimulator import SoccerTeam,Player

team2j = SoccerTeam("team1",[Player("serge",attaqueG),Player("ramos",central)])
team2j2 = SoccerTeam("team2",[Player("pique",goalG),Player("masherano",attaqueG)])
teamREAL = SoccerTeam("team1",[Player("CR7",pointe),Player("ramos",defenseG),Player("marcelo",lateralG),Player("navas",goalG)])
teamPSG4 = SoccerTeam("team1",[Player("trapp",goalG),Player("silva",central),Player("aurier",defenseG),Player("zlatan",attaqueG)])
team1j = SoccerTeam("team1",[Player("serge",attaqueG)])
team12j = SoccerTeam("team1",[Player("ert",central)])

teama4 = SoccerTeam("test",[Player("t",central),Player("s",defenseG),Player("a",millieu),Player("z",pointe)])