""" Permet de jouer et d'entrainer une strategie
    * changer les strategies ajoutees
    * utilisation : python entrainer prefix_fichier_exemple
    par defaut ajoute au fichier d'exemples sil existe deja
    (extension : .exp pour le fichier exemple)
"""

from soccersimulator import SoccerMatch, show, SoccerTeam,Player,KeyboardStrategy
from strategies import FonceurStrategy, DefenseStrategy, RandomStrategy
import sys

if __name__=="__main__":
    prefix = "tree"
    if len(sys.argv)>1:
        prefix = sys.argv[1]
    strat_key = KeyboardStrategy()
    strat_key.add("a",RandomStrategy())
    strat_key.add("z",FonceurStrategy())
    strat_key.add("e",DefenseStrategy())
    team_noob = SoccerTeam("keyb",[Player("KBs", strat_key),Player("Defense",DefenseStrategy())])
    team_bad = SoccerTeam("foncteam",[Player("Fonceur",FonceurStrategy()),Player("Defense", DefenseStrategy())])
    match = SoccerMatch(team_noob,team_bad,1000)
    show(match)
    strat_key.write(prefix+".exp",True)
