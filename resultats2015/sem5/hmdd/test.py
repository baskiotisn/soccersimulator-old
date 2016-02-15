from soccersimulator import show
from soccersimulator import SoccerMatch
from team import lalya1, lalya2, lalya4, lalya1bis

match_lalya1 = SoccerMatch(lalya1, lalya1)
match_lalya2 = SoccerMatch(lalya2, lalya2)
match_lalya4 = SoccerMatch(lalya4, lalya4)


match_lalya5 = SoccerMatch(lalya2, lalya2)
if __name__ == "__main__":
    show(match_lalya5)
