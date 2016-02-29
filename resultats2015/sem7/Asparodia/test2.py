from strategy import MaStrategyFonceur
from strategy import MaStrategyDefensive
from strategy import MaStrategyCampeur
from strategy import MaStrategyGoal
from strategy import MaStrategyUtilitaire
from soccersimulator import DecisionTreeClassifier, SoccerMatch, show, SoccerTeam,Player
from tree import gen_features
import cPickle

tree = cPickle.load(file("./tree.pkl"))
dic = {"Random":RandomStrategy(),"Fonceur":FonceurStrategy(),"Defense":DefenseStrategy()}
treeIA = DTreeStrategy(tree,dic,gen_features)

team_noob = SoccerTeam("keyb",[Player("treeIA", treeIA),Player("Defense",RandomStrategy())])
team_bad = SoccerTeam("foncteam",[Player("Fonceur",FonceurStrategy()),Player("Defense", DefenseStrategy())])
match = SoccerMatch(team_noob,team_bad)
show(match)
