from soccersimulator import SoccerBattle, SoccerPlayer, SoccerTeam
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from soccersimulator import pyglet
from strats import RandomStrategy

team1=SoccerTeam("team1")
team1.add_player(SoccerPlayer("t1j1",RandomStrategy()))
team1.add_player(SoccerPlayer("t1j2",RandomStrategy()))

teams =[team1]



if __name__== "__main__":
	battle=SoccerBattle(team1,team1.copy())
	obs=PygletObserver()
	obs.set_soccer_battle(battle)
	pyglet.app.run()

