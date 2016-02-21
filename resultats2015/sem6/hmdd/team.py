from soccersimulator import SoccerTeam, Player
from coordination import *

t0 = Player("t0", z)
t1 = Player("t1", z)
t2 = Player("t3", z)
essai = Player("essai", passeur)
lalya0 = SoccerTeam("passe", [t0, t1, t2, essai])


t1j1 = Player("t1j1", player_team1)
t1j2 = Player("bete", attaquant)
lalya1 = SoccerTeam("lalya1", [t1j1])
moi = Player("moi", gardien)
lalya1bis = SoccerTeam("lalya1bis", [moi])


t2j1 = Player("t2j1", gardien)
t2j2 = Player("t2j2", player_team2)
lalya2 = SoccerTeam("lalya2", [t2j1, t2j2])

t4j1 = Player("t4j1", defenseur)
t4j2 = Player("t4j2", player_team41)
t4j3 = Player("t4j3", gardien_team4)
t4j4 = Player("t4j4", player_team42)
lalya4 = SoccerTeam("lalya4", [t4j1, t4j2, t4j3, t4j4])
