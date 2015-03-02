from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pickle
import os

from soccersimulator import SoccerStrategy
from strats import *

# Quelques generateurs de features

def distance_ball(state,teamid,playerid):
    return (state.get_team(teamid)[playerid].position-state.ball.position).norm

def distance_mon_but(state,teamid,playerid):
    return (state.get_goal_center(teamid)-state.get_team(teamid)[playerid].position).norm

def distance_autre_but(state,teamid,playerid):
    return (state.get_goal_center(3-teamid)-state.get_team(teamid)[playerid].position).norm

def distance_ball_mon_but(state,teamid,playerid):
    return (state.get_goal_center(teamid)-state.ball.position).norm


def distance_ball_autre_but(state,teamid,playerid):
    return (state.get_goal_center(3-teamid)-state.ball.position).norm


list_fun_features=[distance_ball,distance_mon_but,distance_autre_but,distance_ball_mon_but,distance_ball_autre_but]

# Une fonction de generation de feature.
# np.array permet de transformer en vecteur une liste
def gen_feature_simple(state,teamid,playerid):
    return np.array([f(state,teamid,playerid) for f in list_fun_features])

# Lire les etats contenus dans un fichier
def load_interact(fn):
    states=[]
    with open(fn,"rb") as f:
        while(1):
            try:
                states+=pickle.load(f)
            except EOFError:
                break
    return states

# Apprendre un arbre a partir de la sortie de load_interact, le stocker dans le fichier fn au besoin
def learn_tree(states,fn=None):
    train_set=np.array([gen_feature_simple(s[0],s[1],s[2]) for s in states])
    label_set=np.array([s[3] for s in states])
    tree=DecisionTreeClassifier()
    tree.max_depth=5
    tree.fit(train_set,label_set)
    if fn:
        with open(fn,"wb") as f:
            pickle.dump(tree,f,-1)
    return tree

# Classe generique d'une strategie arbre, fn_tree : nom  de fichier de l'arbre
class TreeStrategy(SoccerStrategy):
    def __init__(self,name,gen_feat,fn_tree,dic_strat):
        self.name=name
        fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),fn_tree)
        self.tree=pickle.load(open(fn,"rb"))
        self.gen_feat=gen_feat
        self.dic_strat=dic_strat
    def compute_strategy(self,state,player,teamid):
        strat = self.tree.predict(self.gen_feat(state,teamid,player.id))[0]
        return self.dic_strat[strat].compute_strategy(state,player,teamid)

#Classe instanciee d'un arbre
class FirstTreeStrategy(TreeStrategy):
    def __init__(self):
        dic_strat_first=dict({"Random":RandomStrategy(),"Fonceur":FonceurStrategy})
        super(FirstTreeStrategy,self).__init__("My First Tree",gen_feature_simple,"first_tree.pkl",dic_strat_first)


if __name__=="__main__":
    states=load_interact("test_interact.pkl")
    learn_tree(states,"first_tree.pkl")
