# -*- coding: utf-8 -*-

from soccersimulator import SoccerPlayer, SoccerTeam, InteractStrategy, TreeStrategy
from strats import RandomStrategy, FonceurStrategy
from apprentissage import *
from apprentissage import gen_feature_simple

team1=SoccerTeam("Fonceur Random")
team1.add_player(SoccerPlayer("Fonceur",FonceurStrategy()))
team1.add_player(SoccerPlayer("Random",RandomStrategy()))

team2=SoccerTeam("Random Random")
team2.add_player(SoccerPlayer("Random 1",RandomStrategy()))
team2.add_player(SoccerPlayer("Random 2",RandomStrategy()))


list_key_player1=['a','z']
list_strat_player1=[RandomStrategy(),FonceurStrategy()]
inter_strat_player1=InteractStrategy(list_key_player1,list_strat_player1,"joueur1")

team3 = SoccerTeam("Interactive")
team3.add_player(SoccerPlayer("Inter 1",inter_strat_player1))
team3.add_player(SoccerPlayer("Rand",RandomStrategy()))

team_tree = SoccerTeam("Team Tree")
treeia=TreeIA(gen_feature_simple,dict({"Random":RandomStrategy(),"Fonceur":FonceurStrategy()}))

### Apprentissage
fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),"myfirsttree.pkl")
treeia.load(fn)
TreeST=TreeStrategy("tree1",treeia)

team_tree.add_player(SoccerPlayer("Tree 1",TreeST))
team_tree.add_player(SoccerPlayer("Tree 2",TreeST))

teams =[team_tree,team1,team2,team3]
