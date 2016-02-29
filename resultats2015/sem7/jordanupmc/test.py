from Strat import *
from team import team1, team2, team4, team11, strat_key 
import cPickle

match=SoccerMatch(team1,team11)
#match.play()
soccersimulator.show(match)

## Sauvegarde des exemples, mettre False a True si concatenation des fichiers
#strat_key.write("test.tree",False)

## Lecture du fichier cree
exemples = KeyboardStrategy.read("./test.tree")
## constitution de la base d'entrainement et des labels
train,labels = build_apprentissage("./test.tree",gen_feat)
## apprentissage de l'arbre
tree = apprendre_arbre(train,labels)
## sauvegarde de l'arbre
cPickle.dump(tree,file("tree.pkl","w")) #tree.pkl


"""
tournoi=SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team11)
#tournoi.add_team(team4)
#tournoi.play()
soccersimulator.show(tournoi)
   """                         

