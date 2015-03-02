# -*- coding: utf-8 -*-

from soccersimulator import SoccerPlayer, SoccerTeam, InteractStrategy
from strats import RandomStrategy, FonceurStrategy
from apprentissage import FirstTreeStrategy

team1=SoccerTeam("Fonceur Random")
team1.add_player(SoccerPlayer("Fonceur",FonceurStrategy()))
team1.add_player(SoccerPlayer("Random",RandomStrategy()))

team2=SoccerTeam("Random Random")
team2.add_player(SoccerPlayer("Random 1",RandomStrategy()))
team2.add_player(SoccerPlayer("Random 2",RandomStrategy()))


list_key_player1=['a','z']
list_key_player2=['q','s']
list_strat_player1=[RandomStrategy(),FonceurStrategy()]
list_strat_player2=[RandomStrategy(),FonceurStrategy()]
inter_strat_player1=InteractStrategy(list_key_player1,list_strat_player1,"joueur1")
inter_strat_player2=InteractStrategy(list_key_player2,list_strat_player2,"joueur2")

team3 = SoccerTeam("Interactive")
team3.add_player(SoccerPlayer("Inter 1",inter_strat_player1))
team3.add_player(SoccerPlayer("Inter 2",inter_strat_player2))

team_tree = SoccerTeam("Team Tree")
team_tree.add_player(SoccerPlayer("Tree 1",FirstTreeStrategy()))
team_tree.add_player(SoccerPlayer("Tree 2",FirstTreeStrategy()))


teams =[team1,team2,team3,team_tree]
teams=[team_tree]
