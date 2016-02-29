from soccersimulator import show
from soccersimulator import SoccerMatch
from soccersimulator import KeyboardStrategy
from team import lalya1, lalya2, lalya4, lalya1bis, lalya0, lalya0bis
from coordination import *

match_lalya1 = SoccerMatch(lalya1, lalya1)
match_lalya2 = SoccerMatch(lalya2, lalya2)
match_lalya4 = SoccerMatch(lalya4, lalya4)

match_lalya5 = SoccerMatch(lalya0, lalya1bis)

strat = KeyboardStrategy(fn="monfichier.exp") #fn veut dire filename
strat.add("f", fonceur_shooteur)
strat.add("b", buteur)
strat.add("r", runv_goal)
strat.add("t", runv_goal_arr)
#Ensuite on ajoute les joueurs, bref...
t1j1 = Player("t1j1", strat)
dogomet1 = SoccerTeam("dogomet1", [t1j1])
match_dogomet1 = SoccerMatch(dogomet1, lalya1bis)


if __name__ == "__main__":
    show(match_lalya5)
