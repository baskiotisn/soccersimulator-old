from Strat import *
from team import team1, team2, team4, team11 

match=SoccerMatch(team1,team11)
#match.play()
soccersimulator.show(match)
tournoi=SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team11)
#tournoi.add_team(team4)
#tournoi.play()
soccersimulator.show(tournoi)
                            
