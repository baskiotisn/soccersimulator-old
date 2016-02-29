from soccersimulator import SoccerMatch, SoccerTournament,KeyboardStrategy
from soccersimulator import SoccerTeam, Player, show
from strat import *
from soccersimulator import settings, Vector2D,DecisionTreeClassifier
import tools
from soccersimulator import export_graphviz
import cPickle

#team_noob = SoccerTeam("keyb",[Player("KBs", strat_key),Player("Defense",StrategyD())])
#team_bad = SoccerTeam("foncteam",[Player("Fonceur",StrategyA()),Player("Defense", StrategyD())])


## Fonction de generation de descripteurs
def gen_features(state,id_team,id_player):
	mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
	return mystate.attribut_arbre

def build_apprentissage(fn,generator):
    	ex_raw = KeyboardStrategy.read(fn)
   	exemples = []
    	labels = []
    	for x in ex_raw:
    	    exemples.append(gen_features(x[1],x[0][0],x[0][1]))
    	    labels.append(x[0][2])
    	return exemples,labels

def apprendre_arbre(train,labels,depth=5):
    	tree= DecisionTreeClassifier()
    	tree.fit(train,labels)
    	return tree

def affiche_arbre(tree):
    long = 10
    sep1="|"+"-"*(long-1)
    sepl="|"+" "*(long-1)
    sepr=" "*long
    def aux(node,sep):
        if tree.tree_.children_left[node]<0:
            ls ="(%s)" % (", ".join( "%s: %d" %(tree.classes_[i],int(x)) for i,x in enumerate(tree.tree_.value[node].flat)))
            return sep+sep1+"%s\n" % (ls,)
        return (sep+sep1+"X%d<=%0.2f\n"
                +"%s"
                +sep+sep1+"X%d>%0.2f\n"
                +"%s" )% (tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_left[node],sep+sepl),
                                   tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_right[node],sep+sepr))
    return aux(0,"")
	
## constitution de la base d'entrainement et des labels
train,labels = build_apprentissage("./monfichier.exp",gen_features)
## apprentissage de l'arbre
tree = apprendre_arbre(train,labels)
## sauvegarde de l'arbre
cPickle.dump(tree,file("tree.pkl","w"))

## exporter l'arbre en .dot
with file("tree.dot","w") as fn:
	export_graphviz(tree,fn)
## puis utiliser ou dot -Tpdf -o tree.pdf tree.dot pour convertir
## ou aller sur http://www.webgraphviz.com/ et copier le fichier .dot
