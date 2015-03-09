import os
import sys
import imp
import soccersimulator
from soccersimulator import PygletObserver
import shutil
import argparse
import pickle


TARGET_PATH="/tmp/tournoi"

GIT_LIST_2015=[("Benlog","Soccer-AI"),("SebXIII","Projet"),("andrenasturas","2I013"),("AlexandreCasanova","projet"),\
            ("mariene","projet_foot"),("Leynad","ProjetFoot"),("ArezkiSky","Projet-soccer-2I013"),("Maumiz","ProjetSoccer"),\
            ("kabylemak","soccerproject"),("timotheb","projet"),("orangemango","orange-soccer-team")]

def load_from_github(login,project,path=TARGET_PATH):
    # clone le depot github correspondant
        print "Debut import github"
        if not os.path.exists(path):
            os.mkdir(path)
        tmp_path=os.path.join(path,login)
        shutil.rmtree(tmp_path, ignore_errors=True)
        os.mkdir(tmp_path)
        os.system("git clone https://github.com/%s/%s %s " % (login,project,tmp_path))
        print "Fin de l'import github"

def check_date(login,project,path=TARGET_PATH):
    print login
    os.system("git --git-dir=%s/.git log  --format=\"%%Cgreen%%cd %%Creset \"| cut -d \" \" -f 1-3,7| uniq" % (os.path.join(path,login),))


def load_directory(tournament,path):
    path=os.path.realpath(path)
    logins=[login for login in os.listdir(path) if os.path.isdir(os.path.join(path,login))]
    for l in logins:
        tournament.add_club(load_club_directory(path,l))
    return tournament

def load_club_directory(path,login=None):
    projet=path
    if not login:
        projet,login=os.path.split(os.path.realpath(path))

    club = soccersimulator.SoccerClub(login)
    try:
        sys.path.insert(0,projet)
        mymod = __import__(login)
        del sys.path[0]
    except Exception,e:
        print "\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (club.login,str(e))
        print sys.exc_info()[0]
        club._exceptions.append(("Module %s " % (login,),e))
        return club
    print "Equipe de \033[92m%s\033[0m charge, \033[92m%s equipes\033[0m" % (login,len(mymod.teams))
    club.add_teams(mymod.teams)
    if hasattr(mymod,"name"):
        club.name=mymod.name
    return club


CFG_0=dict({"ballBrakeConstant":0.08, "ballBrakeSquare":0.01})
CFG_1=dict({"ballBrakeConstant":0.05, "ballBrakeSquare":0.0025})
CFG_2=dict({"ballBrakeConstant":0.05, "ballBrakeSquare":0.0016})
CFG_3=dict({"ballBrakeConstant":0.04, "ballBrakeSquare":0.0016})
CFG=[CFG_0,CFG_1,CFG_2,CFG_3]

def replay(fn):
    obs=soccersimulator.PygletReplay()
    obs.load(args.replay)
    soccersimulator.pyglet.app.run()

if __name__=="__main__":
    parse = argparse.ArgumentParser(description="Soccersimulator Main")
    parse.add_argument('-config',action='store',default=1,type=int,help="Choose config (1,2)")
    parse.add_argument('-path',action='store',nargs="*",default=None,help="Import directory DIR")
    parse.add_argument('-git',action='store_true',default=False,help="Import github to directory")
    parse.add_argument('-nobattle',action="store_true",default=False,help="Do not play the games")
    parse.add_argument('-nb',action="store",dest='max_teams',type=int,default=2,help="Maximum number of teams per club")
    parse.add_argument('-g', action="store",dest='nbgoals',type=int,default=10,help="Number of goals")
    parse.add_argument('-time', action="store",dest='max_time',type=int,default=2000,help="Max time for a goal")
    parse.add_argument('-nbp',nargs='+',type=int,help="List of type of tournament (number of player, 1,2 or 4)")
    parse.add_argument('-login',nargs='+',default=None,help="List of logins to play")
    parse.add_argument('-club',nargs='+',default=None,help="List of clubs to play")
    parse.add_argument('-team',nargs='+',default=None,help='List of teams to play')
    parse.add_argument('-only',action='store_true',default=False,help="If present, battles only between login|club|team passed as argument")
    parse.add_argument('-score',action="store",default=None,help="Save the scores to file O ")
    parse.add_argument('-save',action="store",default=None,help="Save matches")
    parse.add_argument('-replay',action="store",default=None,help="Watch replay")
    parse.add_argument('-watch',action="store_true",default=False,help="Watch live")
    parse.add_argument('-result',action="store",default=None,help="Print results from score file")
    parse.add_argument('-date',action="store_true",default=False)
    args=parse.parse_args()

    if args.result:
        sc=pickle.load(open(args.result,"rb"))
        print soccersimulator.Score.format_dic_score(sc)
        sys.exit(0)
    if args.replay:
        replay(args.replay)
        sys.exit(0)

    #if args.git:
    #    TARGET_PATH=args.git
    if not args.path:
        args.path=TARGET_PATH
    if type(args.path)!=list:
        args.path=[args.path]
    if not args.nbp:
        args.nbp=[1,2,4]
    cfg=CFG[min(args.config,len(CFG)-1)]
    tournament = soccersimulator.SoccerTournament("Test",[1,2,4],max_teams=args.max_teams,\
            nbgoals=args.nbgoals,max_time=args.max_time,save_fn=args.save,save_score=args.score,cst=cfg)
    git_path=args.path[0]
    if args.git:
        for (login,project) in GIT_LIST_2015:
            load_from_github(login,project,git_path)
    if args.date:
        for (login,project) in GIT_LIST_2015:
            check_date(login,project,git_path)
    if not args.nobattle:
        for path in args.path:
            tournament = load_directory(tournament,path)
        tournament.init_battles()
        obs=None
        if args.watch:
            obs = soccersimulator.PygletTournamentObserver()
            obs.set_tournament(tournament)
        tournament.init_tournament(only=args.only,nbp=args.nbp,login=args.login,club=args.club,team=args.team)
        if obs:
            soccersimulator.pyglet.app.run()
