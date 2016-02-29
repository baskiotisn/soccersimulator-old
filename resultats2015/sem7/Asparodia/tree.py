from soccersimulator import SoccerMatch, SoccerTournament,KeyboardStrategy
from soccersimulator import SoccerTeam, Player, show
from strategy import MaStrategyFonceur
from strategy import MaStrategyDefensive
from strategy import MaStrategyCampeur
from strategy import MaStrategyUtilitaire
from strategy import MaStrategyGoal
from soccersimulator import settings, Vector2D,DecisionTreeClassifier
import cPickle

strat = KeyboardStrategy()
strat.add("a",MaStrategyFonceur())
strat.add("z",MaStrategyDefensive())
strat.add("e",MaStrategyUtilitaire())
strat.add("r",MaStrategyGoal())

team_noob = SoccerTeam("myteam",[Player("Thithi", strat_key),Player("Defense",MaStrategyDefensive())])
team_bad = SoccerTeam("nemesis",[Player("Fonceur",MaStrategyFonceur()),Player("Defense", MaStrategyDefensive())])


## Fonction de generation de descripteurs
def gen_features(state,id_team,id_player):
	Mystate=PlayerStateDeco(state, id_team, id_player)
    ball_pos = Mystate.ball_pos
    my_pos = Mystate.pos()
    my_goal = Mystate.my_goal()
    his_goal = Mystate.his_goal()

	liste_copain=state.get_copain_proche()
    (dist_cop_proche,idteam,idplayer)=liste_copain[1]
    #(dist_cop_loin,idteam,idplayer)=liste_copain[-1]

	liste_adv=state.get_adv_proche()
	(dist_adv_proche,idteam,idplayer)=liste_adv[0]
	#(dist_adv_loin,idteam,idplayer)=liste_adv[-1]

	adv_autour=0
	for (t1,t2,t3) in liste_adv:
		if(t1<15):
			adv_autour+=1
		else:
			continue
	

    return [ball_pos.distance(my_pos),ball_pos.distance(my_goal),ball_pos.distance(his_goal),his_goal.distance(my_pos), my_goal.distance(my_pos), dist_cop_proche, dist_adv_proche,adv_autour]

def build_apprentissage(fn,generator):
    ex_raw = KeyboardStrategy.read(fn)
    exemples = []
    labels = []
    for x in ex_raw:
        exemples.append(generator(x[1],x[0][0],x[0][1]))
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
    cPickle.dump(tree,file("tree.pkl","w"))


