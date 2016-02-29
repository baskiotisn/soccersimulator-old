from soccersimulator import SoccerMatch, SoccerTournament,KeyboardStrategy
from soccersimulator import SoccerTeam, Player, show
from strategies import RandomStrategy,FonceurStrategy,DefenseStrategy
from soccersimulator import settings, Vector2D,DecisionTreeClassifier
from PlayerDecorator import *
from zone import *
from tools import *
import cPickle

## Fonction de generation de descripteurs
def gen_features(state,id_team,id_player):
etat = PlayerDecorator(state,id_team,id_player)
return [etat.distance_ball,etat.distance_my_but,etat.equ_proche_distance, etat.adv_proche_distance, etat .ball_in_my_zone,etat.adv_in_my_zone]

def build_apprentissage(fn,generator):
ex_raw = KeyboardStrategy.read(fn)
exemples = []
labels = []
for x in ex_raw:
exemples.append(gen_generator(x[1],x[0][0],x[0][1]))
labels.append(x[0][2])
return exemples,labels
def apprendre_arbre(train,labels,depth=5):
tree= DecisionTreeClassifier()
tree.fit(train,labels)
return tree
## Match d'entrainement et apprentissage de l'arbre
if False:
match = SoccerMatch(team_noob,team_bad,1000)
show(match)
## Sauvegarde des exemples, mettre False a True si concatenation des fichiers
strat_key.write("test.tree",False)
## Lecture du fichier cree
exemples = KeyboardStrategy.read("./test.tree")
## constitution de la base d'entrainement et des labels
train,labels = build_apprentissage("./test.tree",gen_features)
## apprentissage de l'arbre
tree = apprendre_arbre(train,labels)
## sauvegarde de l'arbre
cPickle.dumps(tree,file("tree.pkl","w"))
