import soccersimulator
from soccersimulator.mdpsoccer import SoccerMatch,SoccerTournament
from soccersimulator.interfaces import MatchWindow, show
from team import team3, team2
#strat.write("monfichier.exp")
match = SoccerMatch(team3, team2)
soccersimulator.show (match)
#match.play()
#tournoi = SoccerTournament() #nbre de joueurs par team
#tournoi.add_team(team1)
#tournoi.add_team(team2)

#soccersimulator.show(tournoi)
