# -*- coding: utf-8 -*-

from soccersimulator import show, DecisionTreeClassifier
from soccersimulator import SoccerTeam, Player, SoccerMatch
#from decisiontree import gen_features
from team import team1,team2,team4
import cPickle
import Asparodia,hmdd,fifa2016,Kabegami,lounisAmazigh,luluperet,redxrdx,Raouf16,Praetonus,nihaakey

from strat import *

# tree = cPickle.load(file("./tree.pkl"))
# dic = {"Attaquant":StrategyA(),"Goal":StrategyG(),"Defenseur":StrategyD()}
# treeIA = DTreeStrategy(tree,dic,gen_features)

# team_noob = SoccerTeam("keyb",[Player("treeIA", treeIA)])#,Player("Goal",StrategyG())])
#team_bad = SoccerTeam("foncteam",[Player("Attaquant",StrategyA()),Player("Defenseur", StrategyD())])
#match = SoccerMatch(team_noob,team_bad)
#show(match)


show(SoccerMatch(team4,nihaakey.team4))


#strat_key.write("monfichier.exp")