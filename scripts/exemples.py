from strategies import FonceurStrategy, DefenseStrategy, RandomStrategy
from decisiontree import DTreeStrategy
from soccersimulator import SoccerMatch, show, SoccerTeam,Player,KeyboardStrategy
from decisiontree import gen_features
import cPickle


#### Arbres de decisions

tree = cPickle.load(file("./test.pkl"))
dic = {"Random":RandomStrategy(),"Fonceur":FonceurStrategy(),"Defense":DefenseStrategy()}
treeStrat = DTreeStrategy(tree,dic,gen_features)


### Entrainer un arbre
strat_key = KeyboardStrategy()
strat_key.add("a",RandomStrategy())
strat_key.add("z",FonceurStrategy())
strat_key.add("e",DefenseStrategy())

team_noob = SoccerTeam("keyb",[Player("KBs", strat_key),Player("Defense",DefenseStrategy())])
team_bad = SoccerTeam("foncteam",[Player("IA", treeStrat),Player("Defense", DefenseStrategy())])
show(SoccerMatch(team_noob,team_bad))