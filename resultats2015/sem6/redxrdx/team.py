# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:29:33 2016

@author: 3200404
"""

 

from strategie import *
from soccersimulator import SoccerTeam,Player

team1 = SoccerTeam("team1",[Player("serge",attaqueG),Player("ramos",goalG)])
team2j = SoccerTeam("team2",[Player("pique",goalG),Player("masherano",attaqueG)])
teamREAL = SoccerTeam("team1",[Player("CR7",attaqueG),Player("ramos",defenseG),Player("marcelo",lateralG),Player("navas",goalG)])
teamPSG4 = SoccerTeam("team1",[Player("zlatan",pointe),Player("silva",defenseG),Player("aurier",lateralG),Player("trapp",goalG)])
team1j = SoccerTeam("team1",[Player("serge",goalG)])