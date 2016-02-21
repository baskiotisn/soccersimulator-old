from soccersimulator import show
from soccersimulator import SoccerMatch
from soccersimulator import KeyboardStrategy
from team import lalya1, lalya2, lalya4, lalya1bis, lalya0
from coordination import *

match_lalya1 = SoccerMatch(lalya1, lalya1)
match_lalya2 = SoccerMatch(lalya2, lalya2)
match_lalya4 = SoccerMatch(lalya4, lalya4)


match_lalya5 = SoccerMatch(lalya4, lalya2)
if __name__ == "__main__":
    strat = KeyboardStrategy(fn="monfichier.exp")
    #fn veut dire filename
    strat.add("d", defenseur)
    #Ensuite on ajoute les joueurs, bref...
    show(match_lalya5)
