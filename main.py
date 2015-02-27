import os
import sys
import imp
import soccersimulator
import shutil
import argparse
import pickle


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
        print sys.exc_info()[0]
        club._exceptions.append(("Module %s " % (login,),e))
        return club

    print "Equipe de \033[92m%s\033[0m charge, \033[92m%s equipes\033[0m" % (login,len(mymod.teams))
    club.add_teams(mymod.teams)
    if hasattr(mymod,"name"):
        club.name=mymod.name
    return club

def load_tournament_git_list(name,nbp,git_list,git_import=True,max_teams=5):
    tournament = soccersimulator.SoccerTournament(name,nbp,max_teams=max_teams)
    for (login,project) in git_list:
        club  = load_from_github(login,project,git_import)
        tournament.add_club(club)
    return tournament

def replay(fn):
    obs=soccersimulator.PygletReplay()
    obs.load(args.replay)
    soccersimulator.pyglet.app.run()

if __name__=="__main__":
    parse = argparse.ArgumentParser(description="Soccersimulator Main")
    parse.add_argument('-git',action='store_true',default=False,help="Import github")
    parse.add_argument('-nb',action="store",dest='max_teams',type=int,default=2,help="Maximum number of teams per club")
    parse.add_argument('-b', action="store_true",dest='battles',default=False,help="Do tournament")
    parse.add_argument('-g', action="store",dest='nbgoals',type=int,default=10,help="Number of goals")
    parse.add_argument('-time', action="store",dest='max_time',type=int,default=5000,help="Max time for a goal")
    parse.add_argument('-nbp',nargs='+',type=int,help="List of type of tournament (number of player, 1,2 or 4)")
    parse.add_argument('-login',nargs='+',default=None,help="List of logins to play")
    parse.add_argument('-club',nargs='+',default=None,help="List of clubs to play")
    parse.add_argument('-team',nargs='+',default=None,help='List of teams to play')
    parse.add_argument('-only',action='store_true',default=False,help="If present, battles only between login|club|team passed as argument")
    parse.add_argument('-o',action="store",default=None,help="Save the scores to file O ")
    parse.add_argument('-save',action="store",default=None,help="Save matches")
    parse.add_argument('-replay',action="store",default=None,help="Watch replay")
    args=parse.parse_args()
    if not args.nbp:
        args.nbp=[1,2,4]
    if args.replay:
        replay(args.replay)
    else:
        tournament = load_tournament_git_list("Test",args.nbp,GIT_LIST_2015,max_teams=args.max_teams,git_import=args.git)
        if args.save:
            tournament.save_fn=args.save
        if args.battles:
            tournament.init_battles()
            if args.login or args.club or args.team:
                res=tournament.do_some_battles(args.only,args.nbp,args.login,args.club,args.team,args.nbgoals,args.max_time)
                scores = soccersimulator.SoccerTournament.build_scores(res)
                print [(str(s.team),str(s)) for s in sorted(scores.values())]
            else:
                scores=dict()
                res=tournament.do_battles(args.nbgoals,args.max_time)
                for nbp,btl in res.items():
                    print '%d tournament:' % (nbp,)
                    scores[nbp]=soccersimulator.SoccerTournament.build_scores(btl)
                    print '\n'.join(["%s (%s) : %s" % (t[2],t[0],str(s))\
                        for t,s in sorted(scores[nbp].items())])
            if args.o:
                with open(args.o,"wb") as f:
                    pickle.dump(scores,f)
