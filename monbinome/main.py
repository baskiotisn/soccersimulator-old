# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:04:42 2015

@author: baskiotisn
"""



from soccersimulator import pyglet
from soccersimulator import PygletObserver
from soccersimulator import SoccerBattle
from monequipe import teams
from copy import deepcopy

team1=teams[0]
if len(teams)>1:
    team2=teams[1]
else:
    team2=deepcopy(team1)
battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()
    
