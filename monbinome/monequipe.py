from soccersimulator import SoccerBattle, SoccerPlayer, SoccerTeam
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from soccersimulator import pyglet
from strats import RandomStrategy
from copy import deepcopy
team1=SoccerTeam("team1")
team1.add_player(SoccerPlayer("t1j1",RandomStrategy()))
team1.add_player(SoccerPlayer("t1j2",RandomStrategy()))

teams =[team1,deepcopy(team1)]
