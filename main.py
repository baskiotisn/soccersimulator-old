import os
import sys
import imp
import soccersimulator
import shutil

TARGET_PATH="/tmp/tournoi"

GIT_LIST_2015=[("Benlog","Soccer-AI"),("SebXIII","Projet"),("andrenasturas","2I013"),("AlexandreCasanova","projet"),\
            ("mariene","projet_foot"),("Leynad","ProjetFoot"),("ArezkiSky","Projet-soccer-2I013"),("Maumiz","ProjetSoccer"),\
            ("kabylemak","soccerproject"),("timotheb","projet"),("orangemango","orange-soccer-team")]


def load_from_github(login,project,git_import=True):
    # clone le depot github correspondant
    if git_import:
        print "Debut import github"
        if not os.path.exists(TARGET_PATH):
            os.mkdir(TARGET_PATH)
        tmp_path=os.path.join(TARGET_PATH,login)
        shutil.rmtree(tmp_path, ignore_errors=True)
        os.mkdir(tmp_path)
        os.system("git clone https://github.com/%s/%s %s " % (login,project,tmp_path))
        print "Fin de l'import github"

    club = soccersimulator.SoccerClub(login)
    try:
        sys.path.insert(0, TARGET_PATH)
        mymod = __import__(login)
        del sys.path[0]
    except Exception, e:
        print "\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (club.login,str(e))
        club._exceptions.append(("Module %s " % (login,),e))
        return club

    print "Equipe de \033[92m%s\033[0m charge, \033[92m%s equipes\033[0m" % (login,len(mymod.teams))
    club.add_teams(mymod.teams)
    if hasattr(mymod,"name"):
        club.name=mymod.name
    return club

def load_tournament_git_list(name,git_list,git_import=True):
    tournament = soccersimulator.SoccerTournament(name)
    for (login,project) in git_list:
        club  = load_from_github(login,project,git_import)
        tournament.add_club(club)
    return tournament


if __name__=="__main__":
    tournament = load_tournament_git_list("Test",GIT_LIST_2015)
    tournament.init_battles()
    tournament.do_battles()
